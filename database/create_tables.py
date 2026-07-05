from database.db import connect

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            racer_id INTEGER,
            name TEXT,
            grade TEXT,
            branch TEXT
        )
    """)
    conn.commit()
    conn.close()
