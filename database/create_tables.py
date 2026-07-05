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
        cur.execute("""
　　　　　　　　CREATE TABLE IF NOT EXISTS races (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                race_code TEXT UNIQUE,
                race_date TEXT,
                stadium TEXT,
                race_no INTEGER,
                race_type TEXT
　　　　　　　　) 
        cur.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    race_id INTEGER,
    boat_no INTEGER,
    racer_id INTEGER,
    motor_no INTEGER
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS odds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    race_id INTEGER,
    bet_type TEXT,
    combination TEXT,
    odds REAL
)
""")
    
    conn.commit()
    conn.close()
