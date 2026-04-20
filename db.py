import sqlite3

def init_db():
    conn = sqlite3.connect("scanner.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS scans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_scan(url, result):
    conn = sqlite3.connect("scanner.db")
    c = conn.cursor()

    c.execute("INSERT INTO scans(url, result) VALUES (?, ?)", (url, str(result)))

    conn.commit()
    conn.close()
