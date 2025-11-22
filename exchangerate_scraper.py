"""
ExchangeRate-API Real Rates
"""
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class ExchangeRateScraper:
    def __init__(self):
        self.api_key = os.getenv('EXCHANGERATE_API_KEY')
        self.base_url = f"https://v6.exchangerate-api.com/v6/{self.api_key}/pair"
    
    def get_rate(self, from_currency="USD", to_currency="MXN", amount=500.0):
        """Get real exchange rate"""
        try:
            url = f"{self.base_url}/{from_currency}/{to_currency}/{amount}"
            
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data['result'] == 'success':
                    rate = data['conversion_rate']
                    converted = data['conversion_result']
                    
                    print(f"✅ REAL Rate: {from_currency}/{to_currency} = {rate}")
                    print(f"   ${amount} {from_currency} = {converted:.2f} {to_currency}")
                    
                    return {
                        "success": True,
                        "from": from_currency,
                        "to": to_currency,
                        "rate": rate,
                        "amount": amount,
                        "converted": converted,
                        "timestamp": datetime.now().isoformat(),
                        "source": "exchangerate-api (REAL)"
                    }
            
            return {"success": False, "error": f"Status {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    scraper = ExchangeRateScraper()
    
    print("\n🔍 Testing Real Exchange Rates:\n")
    
    # USD to MXN
    result1 = scraper.get_rate("USD", "MXN", 500)
    
    # USD to COP
    result2 = scraper.get_rate("USD", "COP", 500)
    
    # USD to VES
    result3 = scraper.get_rate("USD", "VES", 500)