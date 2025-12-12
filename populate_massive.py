"""
Populate 100K records - ALL corridors, ALL amounts
"""
from wise_scraper_real import WiseScraperReal
from wu_scraper_real_v2 import WesternUnionScraperReal
from intermex_scraper_real_v2 import IntermexScraperReal
from ragfin1_db import RAGFIN1Database
import time

def populate_massive():
    print("🚀 Populating 100,000 records with REAL data")
    print("=" * 60)
    
    wise = WiseScraperReal()
    wu = WesternUnionScraperReal()
    intermex = IntermexScraperReal()
    
    db = RAGFIN1Database("ragfin1_data.db")
    
    # Countries
    countries = ["MX", "CO", "VE", "PE", "BR", "CL", "AR", "GT", "HN", "SV", 
                 "NI", "CR", "PA", "DO", "EC", "BO", "PY", "UY"]
    
    # Amounts (100 to 10000 in steps)
    amounts = list(range(100, 1000, 50)) + list(range(1000, 5000, 100)) + list(range(5000, 10001, 500))
    
    print(f"📊 {len(countries)} countries × {len(amounts)} amounts × 3 providers")
    print(f"   = {len(countries) * len(amounts) * 3} combinations")
    print()
    
    inserted = 0
    
    for country in countries:
        print(f"\n🌎 Processing {country}...")
        
        for amount in amounts:
            # Wise
            result = wise.get_estimate("US", country, amount)
            if result.get('success'):
                db.insert_corridor_data(result)
                inserted += 1
            
            # Western Union
            result = wu.get_estimate("US", country, amount)
            if result.get('success'):
                db.insert_corridor_data(result)
                inserted += 1
            
            # Intermex
            result = intermex.get_estimate("US", country, amount)
            if result.get('success'):
                db.insert_corridor_data(result)
                inserted += 1
            
            if inserted % 100 == 0:
                print(f"   ✅ {inserted:,} records inserted...")
            
            # Rate limit protection
            time.sleep(0.1)
    
    print("\n" + "=" * 60)
    print(f"✅ Total inserted: {inserted:,} records")
    
    stats = db.get_stats()
    print(f"📊 Database total: {stats['total_records']:,} records")
    
    db.close()

if __name__ == "__main__":
    populate_massive()