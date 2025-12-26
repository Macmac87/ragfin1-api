"""
Populate RAGFIN1 with Guatemala (GT) data
"""
from wu_scraper_GT import WesternUnionScraperGT
from wise_scraper_GT import WiseScraperGT
from intermex_scraper_GT import IntermexScraperGT
from remitly_scraper_GT import RemitlyScraperGT
from ragfin1_db import RAGFIN1Database
import json

def populate_guatemala():
    print("🚀 Populating RAGFIN1 Database - GUATEMALA (GT)")
    print("=" * 60)
    
    wu = WesternUnionScraperGT()
    wise = WiseScraperGT()
    intermex = IntermexScraperGT()
    remitly = RemitlyScraperGT()
    
    db = RAGFIN1Database("ragfin1.db")
    
    # Multiple amounts to get good data distribution
    corridors = [
        {"origin": "US", "destination": "GT", "amount": 100},
        {"origin": "US", "destination": "GT", "amount": 200},
        {"origin": "US", "destination": "GT", "amount": 300},
        {"origin": "US", "destination": "GT", "amount": 500},
        {"origin": "US", "destination": "GT", "amount": 750},
        {"origin": "US", "destination": "GT", "amount": 1000},
        {"origin": "US", "destination": "GT", "amount": 1500},
        {"origin": "US", "destination": "GT", "amount": 2000},
    ]
    
    print(f"📊 Scraping {len(corridors)} amounts for Guatemala...\n")
    
    all_results = []
    
    print("✅ Western Union (GT)...")
    wu_results = wu.compare_corridors(corridors)
    all_results.extend(wu_results)
    print(f"   ✅ {len(wu_results)} records\n")
    
    print("✅ Wise (GT)...")
    wise_results = wise.compare_corridors(corridors)
    all_results.extend(wise_results)
    print(f"   ✅ {len(wise_results)} records\n")
    
    print("✅ Intermex (GT)...")
    intermex_results = intermex.compare_corridors(corridors)
    all_results.extend(intermex_results)
    print(f"   ✅ {len(intermex_results)} records\n")
    
    print("✅ Remitly (GT) - NEW PROVIDER...")
    remitly_results = remitly.compare_corridors(corridors)
    all_results.extend(remitly_results)
    print(f"   ✅ {len(remitly_results)} records\n")
    
    print("=" * 60)
    print("💾 Inserting Guatemala data into database...")
    
    inserted = 0
    for result in all_results:
        if result.get('success'):
            row_id = db.insert_corridor_data(result)
            inserted += 1
            p = result['provider']
            o = result['origin']
            d = result['destination']
            a = result['send_amount']
            print(f"✅ {p:15} {o} → {d} (${a:6.0f}) - Row {row_id}")
    
    print("=" * 60)
    print(f"✅ Successfully inserted {inserted} Guatemala records")
    
    stats = db.get_stats()
    print(f"📊 Total records in database: {stats['total_records']}")
    
    db.close()
    print("\n✅ Guatemala data populated successfully!")

if __name__ == "__main__":
    populate_guatemala()
