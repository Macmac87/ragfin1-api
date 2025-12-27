from ragfin1_db import RAGFIN1Database
from wu_scraper_SV import WesternUnionScraperSV
from wise_scraper_SV import WiseScraperSV
from intermex_scraper_SV import IntermexScraperSV
from remitly_scraper_SV import RemitlyScraperSV
import time

def populate_el_salvador():
    """Populate database with El Salvador corridor data"""
    
    print("=" * 50)
    print("POPULATING EL SALVADOR (SV) DATA")
    print("=" * 50)
    
    # Initialize scrapers
    wu = WesternUnionScraperSV()
    wise = WiseScraperSV()
    intermex = IntermexScraperSV()
    remitly = RemitlyScraperSV()
    
    # Initialize database
    db = RAGFIN1Database("ragfin1.db")
    
    # Test amounts for US -> SV corridor
    corridors = [
        {"origin": "US", "destination": "SV", "amount": 100},
        {"origin": "US", "destination": "SV", "amount": 200},
        {"origin": "US", "destination": "SV", "amount": 300},
        {"origin": "US", "destination": "SV", "amount": 500},
        {"origin": "US", "destination": "SV", "amount": 750},
        {"origin": "US", "destination": "SV", "amount": 1000},
        {"origin": "US", "destination": "SV", "amount": 1500},
        {"origin": "US", "destination": "SV", "amount": 2000},
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
                    print(f"✓ Inserted (Fee: ${data['fee']})")
                    total_inserted += 1
                else:
                    print(f"✗ Failed")
                    
                time.sleep(0.5)
                
            except Exception as e:
                print(f"✗ Error: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"EL SALVADOR DATA POPULATION COMPLETE")
    print(f"Total records inserted: {total_inserted}")
    print("=" * 50)

if __name__ == "__main__":
    populate_el_salvador()