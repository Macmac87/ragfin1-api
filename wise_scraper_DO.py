import requests
from datetime import datetime
from exchangerate_scraper import ExchangeRateScraper

class WiseScraperDO:
    def __init__(self):
        self.provider = "Wise"
        self.rate_scraper = ExchangeRateScraper()
        
    def get_estimate(self, origin: str, destination: str, amount: float):
        """
        Get Wise estimate for Dominican Republic
        Origin: US, Destination: DO, Currency: DOP
        """
        try:
            # Get real market rate USD -> DOP
            rate_data = self.rate_scraper.get_rate("USD", "DOP", amount)
            if not rate_data.get("success"):
                return None
            real_rate = rate_data["rate"]
            
            # Wise uses real rate (minimal markup ~0.5%)
            wise_markup = 0.995
            wise_rate = real_rate * wise_markup
            
            # Wise fee structure (lower fees, better rates)
            if amount <= 100:
                fee = 3.50
            elif amount <= 300:
                fee = 5.00
            elif amount <= 500:
                fee = 7.50
            elif amount <= 1000:
                fee = 12.00
            else:
                fee = 18.00
            
            # Calculate amounts
            amount_to_convert = amount - fee
            recipient_gets = amount_to_convert * wise_rate
            
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
                "exchange_rate": wise_rate,
                "recipient_gets": round(recipient_gets, 2),
                "effective_rate": round(effective_rate, 2),
                "timestamp": datetime.now().isoformat(),
                "corridor": f"{origin}-{destination}"
            }
            
        except Exception as e:
            print(f"Error getting Wise estimate for DO: {str(e)}")
            return None

# Test
if __name__ == "__main__":
    scraper = WiseScraperDO()
    result = scraper.get_estimate("US", "DO", 100)
    if result:
        print(f"\nWise US -> Dominican Republic")
        print(f"Send: ${result['send_amount']}")
        print(f"Fee: ${result['fee']}")
        print(f"Rate: {result['exchange_rate']:.4f}")
        print(f"Recipient gets: {result['recipient_gets']:.2f} DOP")