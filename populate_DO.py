from ragfin1_db import RAGFIN1Database
from wu_scraper_DO import WesternUnionScraperDO
from wise_scraper_DO import WiseScraperDO
from intermex_scraper_DO import IntermexScraperDO
from remitly_scraper_DO import RemitlyScraperDO
import time

def populate_dominican_republic():
    """Populate database with Dominican Republic corridor data"""
    
    print("=" * 50)
    print("POPULATING DOMINICAN REPUBLIC (DO) DATA")
    print("=" * 50)
    
    # Initialize scrapers
    wu = WesternUnionScraperDO()
    wise = WiseScraperDO()
    intermex = IntermexScraperDO()
    remitly = RemitlyScraperDO()
    
    # Initialize database
    db = RAGFIN1Database("ragfin1.db")
    
    # Test amounts for US -> DO corridor
    corridors = [
        {"origin": "US", "destination": "DO", "amount": 100},
        {"origin": "US", "destination": "DO", "amount": 200},
        {"origin": "US", "destination": "DO", "amount": 300},
        {"origin": "US", "destination": "DO", "amount": 500},
        {"origin": "US", "destination": "DO", "amount": 750},
        {"origin": "US", "destination": "DO", "amount": 1000},
        {"origin": "US", "destination": "DO", "amount": 1500},
        {"origin": "US", "destination": "DO", "amount": 2000},
    ]
    
    scrapers = [
        ("Western Union", wu),
        ("Wise", wise),
        ("Intermex", intermex),
        ("Remitly", remitly)
    ]
    
    total_inserted = 0
    
    for corridor in corridors:
        origin = corridor["origin"]
        destination = corridor["destination"]
        amount = corridor["amount"]
        
        print(f"\n--- Processing ${amount} {origin} -> {destination} ---")
        
        for provider_name, scraper in scrapers:
            try:
                print(f"  Scraping {provider_name}...", end=" ")
                data = scraper.get_estimate(origin, destination, amount)
                
                if data:
                    db.insert_corridor_data(data)
                    print(f"✓ Inserted (Fee: ${data['fee']}, Rate: {data['exchange_rate']:.2f})")
                    total_inserted += 1
                else:
                    print(f"✗ Failed")
                    
                time.sleep(0.5)
                
            except Exception as e:
                print(f"✗ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"DOMINICAN REPUBLIC DATA POPULATION COMPLETE")
    print(f"Total records inserted: {total_inserted}")
    print("=" * 50)

if __name__ == "__main__":
    populate_dominican_republic()