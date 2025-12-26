"""
Wise USA->Guatemala with REAL rates
"""
from exchangerate_scraper import ExchangeRateScraper
from typing import Dict, List
from datetime import datetime

class WiseScraperGT:
    def __init__(self):
        self.rate_scraper = ExchangeRateScraper()
    
    def get_estimate(self, origin: str = "US", destination: str = "GT", amount: float = 500.0) -> Dict:
        """Wise with REAL exchange rates for Guatemala"""
        
        # Get REAL rate for GTQ
        rate_data = self.rate_scraper.get_rate("USD", "GTQ", amount)
        if not rate_data['success']:
            return {"success": False, "error": "Rate fetch failed"}
        
        rate = rate_data['rate']
        
        # Wise uses mid-market rate (no markup)
        wise_rate = rate
        converted = amount * wise_rate
        
        # Wise fee structure (percentage-based)
        if amount <= 500:
            fee = amount * 0.008  # 0.8%
        elif amount <= 1000:
            fee = amount * 0.007  # 0.7%
        elif amount <= 5000:
            fee = amount * 0.006  # 0.6%
        else:
            fee = amount * 0.005  # 0.5%
        
        # Minimum fee
        if fee < 3.00:
            fee = 3.00
        
        return {
            "success": True,
            "provider": "Wise",
            "origin": origin,
            "destination": destination,
            "send_amount": amount,
            "fee": round(fee, 2),
            "exchange_rate": round(wise_rate, 4),
            "total_cost": round(amount + fee, 2),
            "recipient_receives": round(converted, 2),
            "estimated_delivery": "1-2 business days",
            "delivery_method": "Bank transfer",
            "timestamp": datetime.now().isoformat(),
            "data_source": "REAL mid-market rate",
            "note": "Real mid-market rate + low percentage fee"
        }
    
    def compare_corridors(self, corridors: List[Dict]) -> List[Dict]:
        results = []
        for corridor in corridors:
            result = self.get_estimate(
                origin=corridor.get('origin', 'US'),
                destination=corridor.get('destination', 'GT'),
                amount=corridor.get('amount', 500.0)
            )
            results.append(result)
        return results

if __name__ == "__main__":
    scraper = WiseScraperGT()
    result = scraper.get_estimate("US", "GT", 500)
    print("\n" + "="*60)
    print("WISE - USA -> GUATEMALA")
    print("="*60)
    for k, v in result.items():
        print(f"{k}: {v}")
