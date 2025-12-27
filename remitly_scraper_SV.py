from datetime import datetime

class RemitlyScraperSV:
    def __init__(self):
        self.provider = "Remitly"
        
    def get_estimate(self, origin: str, destination: str, amount: float):
        """
        Get Remitly estimate for El Salvador
        Origin: US, Destination: SV, Currency: USD (dollarized)
        NO exchange rate needed - only fees
        """
        try:
            # El Salvador uses USD - no conversion needed
            # Remitly flat fee advantage
            fee = 3.99  # Flat fee for all amounts
            
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
            print(f"Error getting Remitly estimate for SV: {str(e)}")
            return None

# Test
if __name__ == "__main__":
    scraper = RemitlyScraperSV()
    result = scraper.get_estimate("US", "SV", 100)
    if result:
        print(f"\nRemitly US -> El Salvador")
        print(f"Send: ${result['send_amount']}")
        print(f"Fee: ${result['fee']}")
        print(f"Recipient gets: ${result['recipient_gets']}")