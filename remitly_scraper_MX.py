from datetime import datetime
from exchangerate_scraper import ExchangeRateScraper

class RemitlyScraperMX:
    def __init__(self):
        self.provider = "Remitly"
        self.rate_scraper = ExchangeRateScraper()
        
    def get_estimate(self, origin: str, destination: str, amount: float):
        try:
            rate_data = self.rate_scraper.get_rate("USD", "MXN", amount)
            if not rate_data.get("success"):
                return None
            real_rate = rate_data["rate"]
            
            remitly_markup = 0.975
            remitly_rate = real_rate * remitly_markup
            
            fee = 3.99
            
            amount_to_convert = amount - fee
            recipient_gets = amount_to_convert * remitly_rate
            effective_rate = recipient_gets / amount if amount > 0 else 0
            
            return {
                "provider": self.provider,
                "origin": origin,
                "destination": destination,
                "origin_currency": "USD",
                "destination_currency": "MXN",
                "send_amount": amount,
                "fee": fee,
                "exchange_rate": remitly_rate,
                "recipient_gets": round(recipient_gets, 2),
                "effective_rate": round(effective_rate, 4),
                "timestamp": datetime.now().isoformat(),
                "corridor": f"{origin}-{destination}"
            }
            
        except Exception as e:
            print(f"Error getting Remitly estimate for MX: {str(e)}")
            return None

if __name__ == "__main__":
    scraper = RemitlyScraperMX()
    result = scraper.get_estimate("US", "MX", 100)
    if result:
        print(f"\nRemitly US -> Mexico")
        print(f"Send: ${result['send_amount']}")
        print(f"Fee: ${result['fee']}")
        print(f"Rate: {result['exchange_rate']:.4f}")
        print(f"Recipient gets: {result['recipient_gets']:.2f} MXN")