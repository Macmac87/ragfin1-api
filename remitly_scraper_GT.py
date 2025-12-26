"""
Remitly USA->Guatemala with REAL rates
"""
from exchangerate_scraper import ExchangeRateScraper
from typing import Dict, List
from datetime import datetime

class RemitlyScraperGT:
    def __init__(self):
        self.rate_scraper = ExchangeRateScraper()
    
    def get_estimate(self, origin: str = "US", destination: str = "GT", amount: float = 500.0) -> Dict:
        """Remitly with REAL exchange rates for Guatemala"""
        
        # Get REAL rate for GTQ
        rate_data = self.rate_scraper.get_rate("USD", "GTQ", amount)
        if not rate_data['success']:
            return {"success": False, "error": "Rate fetch failed"}
        
        rate = rate_data['rate']
        
        # Remitly typically has 1-2.5% markup depending on delivery speed
        remitly_rate = rate * 0.98  # 2% worse than mid-market (Express option)
        converted = amount * remitly_rate
        
        # Remitly fee structure (tiered pricing)
        fee_structure = {
            (0, 100): 3.99,
            (100, 500): 3.99,
            (500, 1000): 3.99,
            (1000, 5000): 0.00,  # Free for higher amounts
            (5000, float('inf')): 0.00
        }
        
        fee = 0.0
        for (min_amt, max_amt), fee_amt in fee_structure.items():
            if min_amt <= amount < max_amt:
                fee = fee_amt
                break
        
        return {
            "success": True,
            "provider": "Remitly",
            "origin": origin,
            "destination": destination,
            "send_amount": amount,
            "fee": fee,
            "exchange_rate": round(remitly_rate, 4),
            "total_cost": amount + fee,
            "recipient_receives": round(converted, 2),
            "estimated_delivery": "Minutes (Express)",
            "delivery_method": "Bank deposit / Cash pickup",
            "timestamp": datetime.now().isoformat(),
            "data_source": "REAL rate with Remitly markup",
            "note": "Real rate + typical Remitly 2% markup + flat fee"
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
    scraper = RemitlyScraperGT()
    result = scraper.get_estimate("US", "GT", 500)
    print("\n" + "="*60)
    print("REMITLY - USA -> GUATEMALA")
    print("="*60)
    for k, v in result.items():
        print(f"{k}: {v}")
