import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import config

class Database:
    def __init__(self, db_path: str = config.DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                asin TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                current_price REAL,
                original_price REAL,
                category TEXT,
                image_url TEXT,
                affiliate_url TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asin TEXT NOT NULL,
                price REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (asin) REFERENCES products (asin)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sent_deals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asin TEXT NOT NULL,
                price REAL NOT NULL,
                discount_percentage REAL NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (asin) REFERENCES products (asin)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_or_update_product(self, product_data: Dict):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (asin, title, current_price, original_price, category, image_url, affiliate_url, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(asin) DO UPDATE SET
                title = excluded.title,
                current_price = excluded.current_price,
                original_price = excluded.original_price,
                category = excluded.category,
                image_url = excluded.image_url,
                affiliate_url = excluded.affiliate_url,
                last_updated = excluded.last_updated
        ''', (
            product_data['asin'],
            product_data['title'],
            product_data['current_price'],
            product_data['original_price'],
            product_data.get('category', ''),
            product_data.get('image_url', ''),
            product_data['affiliate_url'],
            datetime.now()
        ))
        
        cursor.execute('''
            INSERT INTO price_history (asin, price)
            VALUES (?, ?)
        ''', (product_data['asin'], product_data['current_price']))
        
        conn.commit()
        conn.close()
    
    def get_price_history(self, asin: str, days: int = 30) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT price, timestamp
            FROM price_history
            WHERE asin = ? AND timestamp >= datetime('now', '-' || ? || ' days')
            ORDER BY timestamp DESC
        ''', (asin, days))
        
        history = [{'price': row[0], 'timestamp': row[1]} for row in cursor.fetchall()]
        conn.close()
        return history
    
    def get_products_with_price_drops(self, threshold_percentage: float) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.asin, p.title, p.current_price, p.original_price, 
                   p.category, p.image_url, p.affiliate_url,
                   ((p.original_price - p.current_price) / p.original_price * 100) as discount
            FROM products p
            WHERE p.original_price > 0 
            AND ((p.original_price - p.current_price) / p.original_price * 100) >= ?
            AND p.asin NOT IN (
                SELECT asin FROM sent_deals 
                WHERE sent_at >= datetime('now', '-24 hours')
            )
            ORDER BY discount DESC
        ''', (threshold_percentage,))
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'asin': row[0],
                'title': row[1],
                'current_price': row[2],
                'original_price': row[3],
                'category': row[4],
                'image_url': row[5],
                'affiliate_url': row[6],
                'discount_percentage': row[7]
            })
        
        conn.close()
        return products
    
    def mark_deal_as_sent(self, asin: str, price: float, discount: float):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sent_deals (asin, price, discount_percentage)
            VALUES (?, ?, ?)
        ''', (asin, price, discount))
        
        conn.commit()
        conn.close()
    
    def get_all_products(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT asin, title, current_price, original_price, category FROM products')
        
        products = []
        for row in cursor.fetchall():
            products.append({
                'asin': row[0],
                'title': row[1],
                'current_price': row[2],
                'original_price': row[3],
                'category': row[4]
            })
        
        conn.close()
        return products
