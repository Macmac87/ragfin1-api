"""
Populate RAGFIN1 database with data from ALL providers
"""
import sys
sys.path.append('core')

from wu_scraper_v2 import WesternUnionScraperV2
from remitly_scraper import RemitlyScraper
from wise_scraper import WiseScraper
from xoom_scraper import XoomScraper
from ragfin1_db import RAGFIN1Database
import json

def populate_database():
    print("🚀 Populating RAGFIN1 Database - ALL PROVIDERS")
    print("=" * 60)
    
    wu_scraper = WesternUnionScraperV2()
    remitly_scraper = RemitlyScraper()
    wise_scraper = WiseScraper()
    xoom_scraper = XoomScraper()
    
    db = RAGFIN1Database("ragfin1_data.db")
    
    corridors = [
        {"origin": "US", "destination": "MX", "amount": 100},
        {"origin": "US", "destination": "MX", "amount": 500},
        {"origin": "US", "destination": "MX", "amount": 1000},
        {"origin": "US", "destination": "VE", "amount": 500},
        {"origin": "US", "destination": "CO", "amount": 500},
    ]
    
    print(f"📊 Scraping {len(corridors)} corridors across 4 providers...\n")
    
    all_results = []
    
    print("🔵 Scraping Western Union...")
    wu_results = wu_scraper.compare_corridors(corridors)
    all_results.extend(wu_results)
    print(f"   ✅ {len(wu_results)} records\n")
    
    print("🟢 Scraping Remitly...")
    remitly_results = remitly_scraper.compare_corridors(corridors)
    all_results.extend(remitly_results)
    print(f"   ✅ {len(remitly_results)} records\n")
    
    print("🟣 Scraping Wise...")
    wise_results = wise_scraper.compare_corridors(corridors)
    all_results.extend(wise_results)
    print(f"   ✅ {len(wise_results)} records\n")
    
    print("🔴 Scraping Xoom...")
    xoom_results = xoom_scraper.compare_corridors(corridors)
    all_results.extend(xoom_results)
    print(f"   ✅ {len(xoom_results)} records\n")
    
    print("=" * 60)
    print("💾 Inserting into database...")
    
    inserted = 0
    for result in all_results:
        if result.get('success'):
            row_id = db.insert_corridor_data(result)
            inserted += 1
            print(f"✅ Row {row_id}")
    
    print("=" * 60)
    print(f"✅ Successfully inserted {inserted} records")
    
    stats = db.get_stats()
    print(f"📊 Total records: {stats['total_records']}")
    
    db.close()
    print("\n✅ Database populated successfully!")

if __name__ == "__main__":
    populate_database()