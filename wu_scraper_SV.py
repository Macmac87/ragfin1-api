from datetime import datetime

class WesternUnionScraperSV:
    def __init__(self):
        self.provider = "Western Union"
        
    def get_estimate(self, origin: str, destination: str, amount: float):
        """
        Get Western Union estimate for El Salvador
        Origin: US, Destination: SV, Currency: USD (dollarized)
        NO exchange rate needed - only fees
        """
        try:
            # El Salvador uses USD - no conversion needed
            # Only fee structure applies
            if amount <= 100:
                fee = 4.00
            elif amount <= 300:
                fee = 7.00
            elif amount <= 500:
                fee = 9.00
            elif amount <= 1000:
                fee = 14.00
            else:
                fee = 18.00
            
            # Calculate amounts (no exchange rate)
            recipient_gets = amount - fee
            
            # Exchange rate is 1.0 (USD to USD)
            exchange_rate = 1.0
            effective_rate = recipient_gets / amount if amount > 0 else 0
            
            return {
                "provider": self.provider,
                "origin": origin,
                "destination": destination,
                "origin_currency": "USD",
                "destination_currency": "USD",
                "send_amount": amount,
                "fee": fee,
                "exchange_rate": exchange_rate,
                "recipient_gets": round(recipient_gets, 2),
                "effective_rate": round(effective_rate, 4),
                "timestamp": datetime.now().isoformat(),
                "corridor": f"{origin}-{destination}"
            }
            
        except Exception as e:
            print(f"Error getting WU estimate for SV: {str(e)}")
            return None

# Test
if __name__ == "__main__":
    scraper = WesternUnionScraperSV()
    result = scraper.get_estimate("US", "SV", 100)
    if result:
        print(f"\nWestern Union US -> El Salvador")
        print(f"Send: ${result['send_amount']}")
        print(f"Fee: ${result['fee']}")
        print(f"Recipient gets: ${result['recipient_gets']}")