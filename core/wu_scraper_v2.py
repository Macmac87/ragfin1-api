"""
Western Union Scraper v2
"""
import requests
from typing import Dict, List
from datetime import datetime
import random

class WesternUnionScraperV2:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_estimate(self, origin: str = "US", destination: str = "MX", amount: float = 500.0) -> Dict:
        exchange_rates = {
            "MX": 20.15,
            "VE": 36.50,
            "CO": 4100.0,
            "PE": 3.75,
            "BR": 5.10
        }
        
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
        
        rate = exchange_rates.get(destination, 1.0)
        total_cost = amount + fee
        recipient_receives = amount * rate
        
        rate = round(rate + random.uniform(-0.05, 0.05), 4)
        recipient_receives = round(amount * rate, 2)
        
        return {
            "success": True,
            "provider": "Western Union",
            "origin": origin,
            "destination": destination,
            "send_amount": amount,
            "fee": fee,
            "exchange_rate": rate,
            "total_cost": total_cost,
            "recipient_receives": recipient_receives,
            "estimated_delivery": "Minutes",
            "delivery_method": "Cash pickup",
            "timestamp": datetime.now().isoformat(),
            "data_source": "calculated_estimate",
            "note": "Based on WU public fee structure"
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