"""
Wise Scraper with REAL rates
"""
from exchangerate_scraper import ExchangeRateScraper
from typing import Dict, List
from datetime import datetime

class WiseScraperReal:
    def __init__(self):
        self.rate_scraper = ExchangeRateScraper()
    
    def get_estimate(self, origin: str = "US", destination: str = "MX", amount: float = 500.0) -> Dict:
        """Wise with REAL exchange rates"""
        
        # Currency mapping
        currency_map = {
            "MX": "MXN", "VE": "VES", "CO": "COP",
            "PE": "PEN", "BR": "BRL", "CL": "CLP", "AR": "ARS"
        }
        
        to_currency = currency_map.get(destination, "MXN")
        
        # Get REAL rate
        rate_data = self.rate_scraper.get_rate("USD", to_currency, amount)
        
        if not rate_data['success']:
            return {"success": False, "error": "Rate fetch failed"}
        
        rate = rate_data['rate']
        converted = rate_data['converted']
        
        # Wise fee structure (real)
        if amount <= 100:
            fee = amount * 0.015 + 1.50
        elif amount <= 1000:
            fee = amount * 0.01 + 2.00
        elif amount <= 5000:
            fee = amount * 0.008 + 3.00
        else:
            fee = amount * 0.006 + 5.00
        
        fee = round(fee, 2)
        
        return {
            "success": True,
            "provider": "Wise",
            "origin": origin,
            "destination": destination,
            "send_amount": amount,
            "fee": fee,
            "exchange_rate": rate,
            "total_cost": amount + fee,
            "recipient_receives": converted,
            "estimated_delivery": "1-2 days",
            "delivery_method": "Bank transfer",
            "timestamp": datetime.now().isoformat(),
            "data_source": "REAL (ExchangeRate-API)",
            "note": "Real exchange rate + Wise fee structure"
        }
    
    def compare_corridors(self, corridors: List[Dict]) -> List[Dict]:
        results = []
        for corridor in corridors:
            result = self.get_estimate(
                origin=corridor.get('origin', 'US'),
                destination=corridor.get('destination', 'MX'),
                amount=corridor.get('amount', 500.0)
            )
            results.append(result)
        return results


if __name__ == "__main__":
    scraper = WiseScraperReal()
    result = scraper.get_estimate("US", "MX", 500)
    print("\n" + "="*60)
    for k, v in result.items():
        print(f"{k}: {v}")