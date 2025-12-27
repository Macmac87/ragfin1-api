import requests
from datetime import datetime
from exchangerate_scraper import ExchangeRateScraper

class RemitlyScraperDO:
    def __init__(self):
        self.provider = "Remitly"
        self.rate_scraper = ExchangeRateScraper()
        
    def get_estimate(self, origin: str, destination: str, amount: float):
        """
        Get Remitly estimate for Dominican Republic
        Origin: US, Destination: DO, Currency: DOP
        """
        try:
            # Get real market rate USD -> DOP
            rate_data = self.rate_scraper.get_rate("USD", "DOP", amount)
            if not rate_data.get("success"):
                return None
            real_rate = rate_data["rate"]
            
            # Remitly markup: ~2.5% on rate
            remitly_markup = 0.975
            remitly_rate = real_rate * remitly_markup
            
            # Remitly flat fee structure
            if amount <= 100:
                fee = 3.99
            elif amount <= 300:
                fee = 3.99  # Same low fee
            elif amount <= 500:
                fee = 3.99
            elif amount <= 1000:
                fee = 3.99
            else:
                fee = 3.99  # Flat fee advantage
            
            # Calculate amounts
            amount_to_convert = amount - fee
            recipient_gets = amount_to_convert * remitly_rate
            
            # Effective rate
            effective_rate = recipient_gets / amount if amount > 0 else 0
            
            return {
                "provider": self.provider,
                "origin": origin,
                "destination": destination,
                "origin_currency": "USD",
                "destination_currency": "DOP",
                "send_amount": amount,
                "fee": fee,
                "exchange_rate": remitly_rate,
                "recipient_gets": round(recipient_gets, 2),
                "effective_rate": round(effective_rate, 2),
                "timestamp": datetime.now().isoformat(),
                "corridor": f"{origin}-{destination}"
            }
            
        except Exception as e:
            print(f"Error getting Remitly estimate for DO: {str(e)}")
            return None

# Test
if __name__ == "__main__":
    scraper = RemitlyScraperDO()
    result = scraper.get_estimate("US", "DO", 100)
    if result:
        print(f"\nRemitly US -> Dominican Republic")
        print(f"Send: ${result['send_amount']}")
        print(f"Fee: ${result['fee']}")
        print(f"Rate: {result['exchange_rate']:.4f}")
        print(f"Recipient gets: {result['recipient_gets']:.2f} DOP")