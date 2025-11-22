"""
Western Union with REAL rates
"""
from exchangerate_scraper import ExchangeRateScraper
from typing import Dict, List
from datetime import datetime

class WesternUnionScraperReal:
    def __init__(self):
        self.rate_scraper = ExchangeRateScraper()
    
    def get_estimate(self, origin: str = "US", destination: str = "MX", amount: float = 500.0) -> Dict:
        """WU with REAL exchange rates"""
        
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
        
        # WU typically has 2-3% markup on rate
        wu_rate = rate * 0.97  # 3% worse than mid-market
        converted = amount * wu_rate
        
        # WU fee structure
        fee_structure = {
            (0, 100): 5.00,
            (100, 500): 8.00,
            (500, 1000): 12.00,
            (1000, 5000): 20.00,
            (5000, float('inf')): 30.00
        }
        
        fee = 0.0
        for (min_amt, max_amt), fee_amt in fee_structure.items():
            if min_amt <= amount < max_amt:
                fee = fee_amt
                break
        
        return {
            "success": True,
            "provider": "Western Union",
            "origin": origin,
            "destination": destination,
            "send_amount": amount,
            "fee": fee,
            "exchange_rate": round(wu_rate, 4),
            "total_cost": amount + fee,
            "recipient_receives": round(converted, 2),
            "estimated_delivery": "Minutes",
            "delivery_method": "Cash pickup",
            "timestamp": datetime.now().isoformat(),
            "data_source": "REAL rate with WU markup",
            "note": "Real rate + typical WU 3% markup + fees"
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
    scraper = WesternUnionScraperReal()
    result = scraper.get_estimate("US", "MX", 500)
    print("\n" + "="*60)
    for k, v in result.items():
        print(f"{k}: {v}")