import requests
from datetime import datetime
from exchangerate_scraper import ExchangeRateScraper

class IntermexScraperDO:
    def __init__(self):
        self.provider = "Intermex"
        self.rate_scraper = ExchangeRateScraper()
        
    def get_estimate(self, origin: str, destination: str, amount: float):
        """
        Get Intermex estimate for Dominican Republic
        Origin: US, Destination: DO, Currency: DOP
        """
        try:
            # Get real market rate USD -> DOP
            rate_data = self.rate_scraper.get_rate("USD", "DOP", amount)
            if not rate_data.get("success"):
                return None
            real_rate = rate_data["rate"]
            
            # Intermex markup: ~3% on rate
            intermex_markup = 0.970
            intermex_rate = real_rate * intermex_markup
            
            # Intermex fee structure
            if amount <= 100:
                fee = 4.99
            elif amount <= 300:
                fee = 7.99
            elif amount <= 500:
                fee = 9.99
            elif amount <= 1000:
                fee = 14.99
            else:
                fee = 19.99
            
            # Calculate amounts
            amount_to_convert = amount - fee
            recipient_gets = amount_to_convert * intermex_rate
            
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
                "exchange_rate": intermex_rate,
                "recipient_gets": round(recipient_gets, 2),
                "effective_rate": round(effective_rate, 2),
                "timestamp": datetime.now().isoformat(),
                "corridor": f"{origin}-{destination}"
            }
            
        except Exception as e:
            print(f"Error getting Intermex estimate for DO: {str(e)}")
            return None

# Test
if __name__ == "__main__":
    scraper = IntermexScraperDO()
    result = scraper.get_estimate("US", "DO", 100)
    if result:
        print(f"\nIntermex US -> Dominican Republic")
        print(f"Send: ${result['send_amount']}")
        print(f"Fee: ${result['fee']}")
        print(f"Rate: {result['exchange_rate']:.4f}")
        print(f"Recipient gets: {result['recipient_gets']:.2f} DOP")