import sqlite3
from datetime import datetime

def criar_banco():
    """Initialize the database with scores table"""
    conn = sqlite3.connect('game_scores.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT,
        stars INTEGER,
        date TEXT
    )
    ''')
    conn.commit()
    conn.close()

def salvar_score(player_name, stars):
    """Save player score to database"""
    try:
        conn = sqlite3.connect('game_scores.db')
        cursor = conn.cursor()
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
            INSERT INTO scores (player_name, stars, date)
            VALUES (?, ?, ?)
        ''', (player_name, stars, data_atual))
        conn.commit()
    except Exception as e:
        print(f"Error saving score: {e}")
    finally:
        conn.close()

def get_top_scores(limit=10):
    """Retrieve top scores from database"""
    try:
        conn = sqlite3.connect('game_scores.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT player_name, stars, date 
            FROM scores 
            ORDER BY stars DESC 
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall() or None  # Return None if no scores
    except Exception as e:
        print(f"Error fetching scores: {e}")
        return None
    finally:
        conn.close()

# Initialize database when module loads
criar_banco()