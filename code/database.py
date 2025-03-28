import sqlite3
from datetime import datetime


def criar_banco():
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
    try:
        conn = sqlite3.connect('game_scores.db')
        cursor = conn.cursor()
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insere novo registro
        cursor.execute('''
            INSERT INTO scores (player_name, stars, date)
            VALUES (?, ?, ?)
        ''', (player_name, stars, data_atual))

        conn.commit()
    except Exception as e:
        print(f"Erro ao salvar score: {e}")
    finally:
        conn.close()


def get_top_scores(limit=10):
    try:
        conn = sqlite3.connect('game_scores.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT player_name, stars, date 
            FROM scores 
            ORDER BY stars DESC 
            LIMIT ?
        ''', (limit,))
        resultados = cursor.fetchall()
        return resultados if resultados else None  # Retorna None se não houver scores
    except Exception as e:
        print(f"Erro ao buscar scores: {e}")
        return None
    finally:
        conn.close()


# Cria o banco ao importar
criar_banco()