"""
Database utilities for food recognition app
"""
import sqlite3
import os

def get_db_path():
    """Get the database path."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, 'food_app.db')

DB_PATH = get_db_path()

def get_db_connection():
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize SQLite database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # User goals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_goals (
            id INTEGER PRIMARY KEY,
            user_id TEXT DEFAULT 'default_user',
            daily_calories INTEGER DEFAULT 2000,
            daily_protein_g INTEGER DEFAULT 150,
            daily_carbs_g INTEGER DEFAULT 200,
            daily_fat_g INTEGER DEFAULT 65,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Meal logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            user_id TEXT DEFAULT 'default_user',
            dish_id TEXT NOT NULL,
            meal_type TEXT CHECK(meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
            grams INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            notes TEXT
        )
    ''')
    
    # Initialize default user goals if not exists
    cursor.execute('SELECT * FROM user_goals WHERE user_id = ?', ('default_user',))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO user_goals 
            (user_id, daily_calories, daily_protein_g, daily_carbs_g, daily_fat_g)
            VALUES (?, ?, ?, ?, ?)
        ''', ('default_user', 2000, 150, 200, 65))
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def close_db(e=None):
    """Close database connection."""
    db = None
    if db is not None:
        db.close()
