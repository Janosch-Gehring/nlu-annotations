import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS user_data (
        user_id TEXT PRIMARY KEY,
        task TEXT,
        qualified INTEGER DEFAULT 0,
        annotator_group INTEGER DEFAULT 0,
        progress INTEGER DEFAULT 0,
        annotations TEXT DEFAULT "{}",
        data TEXT DEFAULT "{}"
    )''')
    conn.commit()