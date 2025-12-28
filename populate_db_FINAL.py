"""
Populate RAGFIN1 with REAL data
"""
from wise_scraper_real import WiseScraperReal
from wu_scraper_real_v2 import WesternUnionScraperReal
from intermex_scraper_real_v2 import IntermexScraperReal
from remitly_scraper_MX import RemitlyScraperMX
from remitly_scraper_CO import RemitlyScraperCO
from remitly_scraper_BR import RemitlyScraperBR
from remitly_scraper_AR import RemitlyScraperAR
from remitly_scraper_VE import RemitlyScraperVE
from remitly_scraper_CL import RemitlyScraperCL
from remitly_scraper_PE import RemitlyScraperPE
from remitly_scraper_BO import RemitlyScraperBO
from ragfin1_db import RAGFIN1Database
import json

def populate_database():
    print("🚀 Populating RAGFIN1 Database - REAL DATA")
    print("=" * 60)
    
    wise = WiseScraperReal()
    wu = WesternUnionScraperReal()
    intermex = IntermexScraperReal()
    
    # Initialize Remitly scrapers
    remitly_mx = RemitlyScraperMX()
    remitly_co = RemitlyScraperCO()
    remitly_br = RemitlyScraperBR()
    remitly_ar = RemitlyScraperAR()
    remitly_ve = RemitlyScraperVE()
    remitly_cl = RemitlyScraperCL()
    remitly_pe = RemitlyScraperPE()
    remitly_bo = RemitlyScraperBO()
    
    db = RAGFIN1Database("ragfin1_data.db")
    
    corridors = [
        {"origin": "US", "destination": "MX", "amount": 500},
        {"origin": "US", "destination": "MX", "amount": 1000},
        {"origin": "US", "destination": "CO", "amount": 500},
        {"origin": "US", "destination": "VE", "amount": 500},
    ]
    
    print(f"📊 Scraping {len(corridors)} corridors with REAL data...\n")
    
    all_results = []
    
    print("✅ Wise (REAL rates)...")
    wise_results = wise.compare_corridors(corridors)
    all_results.extend(wise_results)
    print(f"   ✅ {len(wise_results)} records\n")
    
    print("✅ Western Union (REAL rates)...")
    wu_results = wu.compare_corridors(corridors)
    all_results.extend(wu_results)
    print(f"   ✅ {len(wu_results)} records\n")
    
    print("✅ Intermex (REAL rates)...")
    intermex_results = intermex.compare_corridors(corridors)
    all_results.extend(intermex_results)
    print(f"   ✅ {len(intermex_results)} records\n")
    
    print("✅ Remitly (REAL rates)...")
    remitly_results = []
    remitly_scrapers = {
        'MX': remitly_mx,
        'CO': remitly_co,
        'BR': remitly_br,
        'AR': remitly_ar,
        'VE': remitly_ve,
        'CL': remitly_cl,
        'PE': remitly_pe,
        'BO': remitly_bo
    }
    
    for corridor in corridors:
        dest = corridor['destination']
        if dest in remitly_scrapers:
            result = remitly_scrapers[dest].get_estimate(
                corridor['origin'],
                corridor['destination'],
                corridor['amount']
            )
            if result:
                result['success'] = True
                remitly_results.append(result)
    
    all_results.extend(remitly_results)
    print(f"   ✅ {len(remitly_results)} records\n")
    
    print("=" * 60)
    print("💾 Inserting into database...")
    
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
    print(f"✅ Successfully inserted {inserted} records with REAL data")
    
    stats = db.get_stats()
    print(f"📊 Total records: {stats['total_records']}")
    
    db.close()
    print("\n✅ Database populated with REAL exchange rates!")

if __name__ == "__main__":
    populate_database()