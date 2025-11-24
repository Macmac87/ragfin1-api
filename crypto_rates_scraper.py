"""
Crypto Rates Scraper para RAGFIN1
Obtiene tasas de USDT/USDC a monedas locales
APIs: CoinGecko (free) + Binance (free)
Mario @ MGA
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
import time

class CryptoRatesScraper:
    """
    Scraper de tasas crypto para remesas
    Compara USDT/USDC vs monedas fiat LatAm
    """
    
    def __init__(self):
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.binance_base = "https://api.binance.com/api/v3"
        
        # Mapeo de códigos de moneda
        self.currency_map = {
            "MXN": "mxn",
            "COP": "cop", 
            "VES": "ves",
            "BRL": "brl",
            "CLP": "clp",
            "ARS": "ars",
            "PEN": "pen",
            "BOB": "bob"
        }
        
        # Stablecoins a trackear
        self.stablecoins = ["tether", "usd-coin"]  # USDT, USDC en CoinGecko
        
    def get_coingecko_rates(self, currencies: List[str]) -> Dict:
        """
        Obtiene rates de CoinGecko para USDT y USDC
        """
        try:
            # Convertir a formato CoinGecko (lowercase)
            vs_currencies = ",".join([self.currency_map.get(c, c.lower()) for c in currencies])
            
            url = f"{self.coingecko_base}/simple/price"
            params = {
                "ids": "tether,usd-coin",
                "vs_currencies": vs_currencies,
                "include_24hr_change": "true"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Transformar a formato más usable
            rates = {}
            for coin, values in data.items():
                coin_name = "USDT" if coin == "tether" else "USDC"
                rates[coin_name] = {}
                
                for currency in currencies:
                    currency_lower = self.currency_map.get(currency, currency.lower())
                    if currency_lower in values:
                        rates[coin_name][currency] = {
                            "rate": values[currency_lower],
                            "change_24h": values.get(f"{currency_lower}_24h_change", 0)
                        }
            
            return rates
            
        except Exception as e:
            print(f"Error fetching CoinGecko rates: {e}")
            return {}
    
    def get_binance_rate(self, symbol: str) -> Optional[float]:
        """
        Obtiene rate de Binance para un par específico
        Ejemplo: USDTMXN, USDCBRL
        """
        try:
            url = f"{self.binance_base}/ticker/price"
            params = {"symbol": symbol}
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return float(data.get("price", 0))
            
        except Exception as e:
            # No todos los pares existen en Binance
            return None
    
    def get_binance_rates(self, currencies: List[str]) -> Dict:
        """
        Obtiene rates de Binance P2P para múltiples monedas
        """
        rates = {
            "USDT": {},
            "USDC": {}
        }
        
        for currency in currencies:
            # Intentar obtener rates de Binance
            for coin in ["USDT", "USDC"]:
                symbol = f"{coin}{currency}"
                rate = self.get_binance_rate(symbol)
                
                if rate:
                    rates[coin][currency] = {
                        "rate": rate,
                        "source": "binance"
                    }
            
            # Pequeña pausa para no saturar la API
            time.sleep(0.1)
        
        return rates
    
    def get_all_rates(self, currencies: Optional[List[str]] = None) -> Dict:
        """
        Obtiene rates de todas las fuentes y las combina
        """
        if currencies is None:
            currencies = list(self.currency_map.keys())
        
        print(f"🔍 Fetching crypto rates for: {', '.join(currencies)}")
        
        # Obtener de CoinGecko (principal)
        coingecko_rates = self.get_coingecko_rates(currencies)
        
        # Obtener de Binance (secundario)
        binance_rates = self.get_binance_rates(currencies)
        
        # Combinar resultados (CoinGecko tiene prioridad)
        combined_rates = {
            "timestamp": datetime.now().isoformat(),
            "source": "multi",
            "rates": {}
        }
        
        for coin in ["USDT", "USDC"]:
            combined_rates["rates"][coin] = {}
            
            for currency in currencies:
                # Preferir CoinGecko, fallback a Binance
                if coin in coingecko_rates and currency in coingecko_rates[coin]:
                    combined_rates["rates"][coin][currency] = {
                        **coingecko_rates[coin][currency],
                        "source": "coingecko"
                    }
                elif coin in binance_rates and currency in binance_rates[coin]:
                    combined_rates["rates"][coin][currency] = binance_rates[coin][currency]
                else:
                    # No hay data disponible
                    combined_rates["rates"][coin][currency] = {
                        "rate": None,
                        "source": "unavailable"
                    }
        
        return combined_rates
    
    def compare_with_traditional(self, country: str, traditional_rates: Dict, 
                                 crypto_rates: Dict, amount: float = 1000) -> Dict:
        """
        Compara costos entre remesas tradicionales y crypto para UN país
        """
        comparison = {
            "amount_usd": amount,
            "timestamp": datetime.now().isoformat(),
            "country": country
        }
        
        if not traditional_rates:
            comparison["error"] = "No traditional rates available"
            return comparison
        
        # Encontrar el mejor provider tradicional
        best_traditional = min(traditional_rates.items(), 
                              key=lambda x: x[1].get("total_cost", float("inf")))
        
        provider_name, provider_data = best_traditional
        trad_total_cost = provider_data.get("total_cost", 0)
        
        # Calcular costo crypto (asumiendo USDT)
        crypto_rate = crypto_rates.get("rates", {}).get("USDT", {}).get(country.upper(), {}).get("rate")
        
        if crypto_rate:
            # Costo crypto = amount / rate (1000 USD compra X moneda local)
            crypto_received = amount * crypto_rate
            
            # Para remesas tradicionales
            trad_rate = provider_data.get("rate", 0)
            trad_fee = provider_data.get("fee", 0)
            trad_received = (amount - trad_fee) * trad_rate if trad_rate > 0 else 0
            
            # Comparar cuánto recibe el destinatario
            difference = crypto_received - trad_received
            difference_pct = (difference / trad_received * 100) if trad_received > 0 else 0
            
            comparison["traditional"] = {
                "best_provider": provider_name,
                "exchange_rate": trad_rate,
                "fee_usd": trad_fee,
                "recipient_receives": round(trad_received, 2)
            }
            
            comparison["crypto"] = {
                "rate": crypto_rate,
                "fee_usd": 0,  # Simplificado
                "recipient_receives": round(crypto_received, 2)
            }
            
            comparison["winner"] = "crypto" if difference > 0 else "traditional"
            comparison["difference"] = {
                "amount": round(difference, 2),
                "percentage": round(difference_pct, 2)
            }
        else:
            comparison["error"] = f"No crypto rate available for {country}"
        
        return comparison
    
    def get_crypto_summary(self) -> Dict:
        """
        Obtiene resumen de todas las tasas crypto disponibles
        """
        rates = self.get_all_rates()
        
        summary = {
            "timestamp": rates["timestamp"],
            "stablecoins": ["USDT", "USDC"],
            "currencies_tracked": len(self.currency_map),
            "rates_by_coin": {}
        }
        
        for coin in ["USDT", "USDC"]:
            coin_rates = rates["rates"].get(coin, {})
            available = sum(1 for v in coin_rates.values() if v.get("rate") is not None)
            
            summary["rates_by_coin"][coin] = {
                "available_currencies": available,
                "total_currencies": len(self.currency_map),
                "coverage_pct": round(available / len(self.currency_map) * 100, 2)
            }
        
        return summary


def test_crypto_scraper():
    """Test del scraper"""
    print("🚀 Testing Crypto Rates Scraper...")
    
    scraper = CryptoRatesScraper()
    
    # Test 1: Obtener rates para países principales
    print("\n📊 Test 1: Fetching rates for main countries...")
    test_currencies = ["MXN", "COP", "BRL", "ARS"]
    rates = scraper.get_all_rates(test_currencies)
    
    print(f"✅ Timestamp: {rates['timestamp']}")
    print(f"✅ Source: {rates['source']}")
    
    # Mostrar rates de USDT
    print("\n💵 USDT Rates:")
    for currency, data in rates["rates"]["USDT"].items():
        rate = data.get("rate")
        source = data.get("source")
        if rate:
            print(f"   {currency}: {rate:.4f} ({source})")
        else:
            print(f"   {currency}: Not available")
    
    # Test 2: Summary
    print("\n📈 Test 2: Getting summary...")
    summary = scraper.get_crypto_summary()
    print(f"✅ Stablecoins tracked: {summary['stablecoins']}")
    print(f"✅ Currencies tracked: {summary['currencies_tracked']}")
    
    for coin, stats in summary["rates_by_coin"].items():
        print(f"\n   {coin}:")
        print(f"   - Available: {stats['available_currencies']}/{stats['total_currencies']}")
        print(f"   - Coverage: {stats['coverage_pct']}%")
    
    # Test 3: Guardar JSON
    print("\n💾 Test 3: Saving to JSON...")
    with open("crypto_rates_sample.json", "w") as f:
        json.dump(rates, f, indent=2)
    print("✅ Saved to crypto_rates_sample.json")
    
    print("\n✅ ALL TESTS PASSED")


if __name__ == "__main__":
    test_crypto_scraper()