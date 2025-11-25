"""
Binance P2P Scraper para RAGFIN1
Obtiene tasas de compra/venta USDT en monedas locales
Mario @ MGA
"""
import requests
from typing import Dict, List, Optional
from datetime import datetime

class BinanceP2PScraper:
    def __init__(self):
        self.base_url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        
        # Mapeo país a moneda fiat
        self.currency_map = {
            "MX": "MXN",
            "CO": "COP",
            "VE": "VES",
            "BR": "BRL",
            "AR": "ARS",
            "CL": "CLP",
            "PE": "PEN",
            "BO": "BOB"
        }
    
    def get_p2p_rate(self, fiat: str, trade_type: str = "BUY", 
                     asset: str = "USDT", amount: float = 1000) -> Dict:
        """
        Obtiene tasa P2P de Binance
        
        trade_type: "BUY" (comprar USDT) o "SELL" (vender USDT)
        """
        
        payload = {
            "asset": asset,
            "fiat": fiat,
            "merchantCheck": False,
            "page": 1,
            "rows": 10,
            "tradeType": trade_type,
            "transAmount": amount
        }
        
        try:
            response = requests.post(
                self.base_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("success") and data.get("data"):
                ads = data["data"]
                
                if not ads:
                    return {"error": f"No P2P ads found for {fiat}"}
                
                # Tomar el mejor rate (primer ad)
                best_ad = ads[0]["adv"]
                
                return {
                    "success": True,
                    "provider": "Binance P2P",
                    "asset": asset,
                    "fiat": fiat,
                    "trade_type": trade_type,
                    "price": float(best_ad["price"]),
                    "min_amount": float(best_ad.get("minSingleTransAmount", 0)),
                    "max_amount": float(best_ad.get("dynamicMaxSingleTransAmount", 0)),
                    "available": float(best_ad.get("surplusAmount", 0)),
                    "payment_methods": best_ad.get("tradeMethods", []),
                    "timestamp": datetime.now().isoformat()
                }
            
            return {"error": "Invalid response from Binance P2P"}
            
        except Exception as e:
            return {"error": f"Binance P2P error: {str(e)}"}
    
    def compare_with_traditional(self, country: str, amount: float = 1000) -> Dict:
        """
        Compara Binance P2P con remesas tradicionales
        """
        fiat = self.currency_map.get(country, country)
        
        # Rate de VENTA de USDT (recibir fiat)
        sell_rate = self.get_p2p_rate(fiat, "SELL", "USDT", amount)
        
        if "error" in sell_rate:
            return sell_rate
        
        # Para remesas: enviar USD, recibir fiat local
        # Si vendes 1000 USDT, recibes X fiat
        received_amount = amount * sell_rate["price"]
        
        return {
            "provider": "Binance P2P",
            "origin": "USD",
            "destination": country,
            "send_amount": amount,
            "fee": 0,
            "exchange_rate": sell_rate["price"],
            "recipient_receives": received_amount,
            "min_amount": sell_rate["min_amount"],
            "max_amount": sell_rate["max_amount"],
            "payment_methods": sell_rate["payment_methods"],
            "timestamp": sell_rate["timestamp"]
        }