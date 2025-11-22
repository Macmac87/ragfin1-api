"""
RAGFIN1 Database Manager
"""
import sqlite3
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class RAGFIN1Database:
    def __init__(self, db_path: str = "ragfin1_data.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()
        print(f"✅ Database connected: {db_path}")
    
    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS corridors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider TEXT NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                send_amount REAL NOT NULL,
                fee REAL NOT NULL,
                exchange_rate REAL NOT NULL,
                total_cost REAL NOT NULL,
                recipient_receives REAL NOT NULL,
                estimated_delivery TEXT,
                delivery_method TEXT,
                timestamp TEXT NOT NULL,
                data_source TEXT,
                note TEXT
            )
        """)
        self.cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_corridor 
            ON corridors(provider, origin, destination, timestamp)
        """)
        self.conn.commit()
    
    def insert_corridor_data(self, data: Dict[str, Any]) -> int:
        self.cursor.execute("""
            INSERT INTO corridors (
                provider, origin, destination, send_amount, fee,
                exchange_rate, total_cost, recipient_receives,
                estimated_delivery, delivery_method, timestamp,
                data_source, note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('provider', 'Unknown'),
            data.get('origin', ''),
            data.get('destination', ''),
            data.get('send_amount', 0.0),
            data.get('fee', 0.0),
            data.get('exchange_rate', 0.0),
            data.get('total_cost', 0.0),
            data.get('recipient_receives', 0.0),
            data.get('estimated_delivery', ''),
            data.get('delivery_method', ''),
            data.get('timestamp', datetime.now().isoformat()),
            data.get('data_source', ''),
            data.get('note', '')
        ))
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_latest_corridor(self, provider: str, origin: str, destination: str, amount: Optional[float] = None) -> Optional[Dict[str, Any]]:
        if amount:
            query = """
                SELECT * FROM corridors
                WHERE provider = ? AND origin = ? AND destination = ? AND send_amount = ?
                ORDER BY timestamp DESC LIMIT 1
            """
            self.cursor.execute(query, (provider, origin, destination, amount))
        else:
            query = """
                SELECT * FROM corridors
                WHERE provider = ? AND origin = ? AND destination = ?
                ORDER BY timestamp DESC LIMIT 1
            """
            self.cursor.execute(query, (provider, origin, destination))
        
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None
    
    def get_stats(self) -> Dict[str, Any]:
        stats = {}
        self.cursor.execute("SELECT COUNT(*) as count FROM corridors")
        stats['total_records'] = self.cursor.fetchone()['count']
        return stats
    
    def close(self):
        if self.conn:
            self.conn.close()
            print("👋 Database connection closed")