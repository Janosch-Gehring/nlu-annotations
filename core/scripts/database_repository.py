import json
import os
import psycopg2
import sqlite3

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def db_connection():
    if os.getenv("DATABASE") == "postgresql":
        conn = psycopg2.connect(
            database = os.getenv("DB_NAME"), 
            user = os.getenv("DB_USER"), 
            host = os.getenv("DB_HOST"),
            password = os.getenv("DB_PASSWORD"),
            port = os.getenv("DB_PORT")
        )
    else:
        # TODO that still needs to be implemented for local testing...
        # (most of what needs to be done is just replacing the %s in queries with ?)
        conn = sqlite3.connect("database.db")
    return conn

# Initialize the database
def init_db():
    conn = db_connection()

    if os.getenv("DATABASE") == "postgresql":
        curr = conn.cursor()
        curr.execute('''
        CREATE TABLE IF NOT EXISTS user_data (
            user_id TEXT PRIMARY KEY,
            task TEXT,
            qualified INTEGER DEFAULT 0,
            annotator_group INTEGER DEFAULT 0,
            progress INTEGER DEFAULT 0,
            annotations JSONB DEFAULT '{}'::jsonb,
            data JSONB DEFAULT '{}'::jsonb
        );''')
        curr.execute('''CREATE TABLE IF NOT EXISTS valid_ids (
            user_id TEXT PRIMARY KEY,
            task TEXT,
            annotator_group INTEGER DEFAULT 0
            )''')
    else:
        conn.execute('''CREATE TABLE IF NOT EXISTS user_data (
            user_id TEXT PRIMARY KEY,
            task TEXT,
            qualified INTEGER DEFAULT 0,
            annotator_group INTEGER DEFAULT 0,
            progress INTEGER DEFAULT 0,
            annotations TEXT DEFAULT "{}",
            data TEXT DEFAULT "{}"
        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS valid_ids (
            user_id TEXT PRIMARY KEY,
            task TEXT,
            annotator_group INTEGER DEFAULT 0
            )''')
    conn.commit()
    conn.close()

def convert_database_to_json():
    connection = db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()
    json_data = []
    for row in rows:
        user_id, task, qualified, annotator_group, progress, annotations, data = row
        json_data.append({"User ID": user_id, "qualified": qualified, "task": task, 
                          "grouping": annotator_group, "progress": progress, 
                          "annotations": annotations, "data": data})
    connection.close()
    
    return json.dumps(json_data, indent=4)