"""
XE.com Real Exchange Rates
"""
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class XERatesScraper:
    def __init__(self):
        self.api_key = os.getenv('XE_API_KEY')
        self.base_url = "https://xecdapi.xe.com/v1/convert_from"
    
    def get_rate(self, from_currency="USD", to_currency="MXN", amount=1.0):
        """Get real exchange rate from XE"""
        try:
            params = {
                "from": from_currency,
                "to": to_currency,
                "amount": amount
            }
            
            headers = {
                "Authorization": f"Basic {self.api_key}"
            }
            
            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                rate = data['to'][0]['mid']
                
                print(f"✅ XE Real Rate: {from_currency}/{to_currency} = {rate}")
                
                return {
                    "success": True,
                    "from": from_currency,
                    "to": to_currency,
                    "rate": rate,
                    "amount": amount,
                    "converted": amount * rate,
                    "timestamp": datetime.now().isoformat(),
                    "source": "xe_api"
                }
            else:
                print(f"❌ XE API error: {response.status_code}")
                return {"success": False, "error": response.text}
                
        except Exception as e:
            print(f"❌ XE Error: {e}")
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    scraper = XERatesScraper()
    result = scraper.get_rate("USD", "MXN", 500)
    print(result)