import requests
from datetime import datetime
from exchangerate_scraper import ExchangeRateScraper

class WesternUnionScraperDO:
    def __init__(self):
        self.provider = "Western Union"
        self.rate_scraper = ExchangeRateScraper()
        
    def get_estimate(self, origin: str, destination: str, amount: float):
        """
        Get Western Union estimate for Dominican Republic
        Origin: US, Destination: DO, Currency: DOP
        """
        try:
            # Get real market rate USD -> DOP
            rate_data = self.rate_scraper.get_rate("USD", "DOP", amount)
            if not rate_data.get("success"):
                return None
            real_rate = rate_data["rate"]
            
            # Western Union markup: 3.5% on rate
            wu_markup = 0.965  # They give 96.5% of real rate
            wu_rate = real_rate * wu_markup
            
            # Fee structure for DO
            if amount <= 100:
                fee = 5.00
            elif amount <= 300:
                fee = 8.00
            elif amount <= 500:
                fee = 10.00
            elif amount <= 1000:
                fee = 15.00
            else:
                fee = 20.00
            
            # Calculate amounts
            amount_to_convert = amount - fee
            recipient_gets = amount_to_convert * wu_rate
            
            # Effective rate (what customer actually gets)
            effective_rate = recipient_gets / amount if amount > 0 else 0
            
            return {
                "provider": self.provider,
                "origin": origin,
                "destination": destination,
                "origin_currency": "USD",
                "destination_currency": "DOP",
                "send_amount": amount,
                "fee": fee,
                "exchange_rate": wu_rate,
                "recipient_gets": round(recipient_gets, 2),
                "effective_rate": round(effective_rate, 2),
                "timestamp": datetime.now().isoformat(),
                "corridor": f"{origin}-{destination}"
            }
            
        except Exception as e:
            print(f"Error getting WU estimate for DO: {str(e)}")
            return None

# Test
if __name__ == "__main__":
    scraper = WesternUnionScraperDO()
    result = scraper.get_estimate("US", "DO", 100)
    if result:
        print(f"\nWestern Union US -> Dominican Republic")
        print(f"Send: ${result['send_amount']}")
        print(f"Fee: ${result['fee']}")
        print(f"Rate: {result['exchange_rate']:.4f}")
        print(f"Recipient gets: {result['recipient_gets']:.2f} DOP")