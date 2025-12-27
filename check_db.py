from ragfin1_db import RAGFIN1Database

db = RAGFIN1Database('ragfin1.db')
stats = db.get_stats()

print(f"\n{'='*50}")
print(f"DATABASE SUMMARY")
print(f"{'='*50}")
print(f"Total records: {stats['total_records']}")

if 'providers' in stats:
    print(f"\nProviders: {', '.join(stats['providers'])}")
if 'corridors' in stats:
    print(f"\nCorridors: {', '.join(stats['corridors'])}")

print(f"\nAll stats keys: {list(stats.keys())}")
print(f"{'='*50}\n")