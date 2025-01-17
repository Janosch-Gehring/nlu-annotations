import json
import sqlite3

# Initialize the database
def init_db():
    pass
    #conn = sqlite3.connect('database.db')
    #conn.execute('''CREATE TABLE IF NOT EXISTS user_data (
    #    user_id TEXT PRIMARY KEY,
    #    task TEXT,
    #    qualified INTEGER DEFAULT 0,
    #    annotator_group INTEGER DEFAULT 0,
    #    progress INTEGER DEFAULT 0,
    #    annotations TEXT DEFAULT "{}",
    #    data TEXT DEFAULT "{}"
    #)''')

    #conn.execute('''CREATE TABLE IF NOT EXISTS valid_ids (
    #    user_id TEXT PRIMARY KEY,
    #    task TEXT,
    #    annotator_group INTEGER DEFAULT 0
    #)''')
    #conn.commit()
    #conn.close()

def convert_database_to_json():
    database_file = 'database.db'
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    # Get all table names in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    database_data = {}

    # Loop through each table to fetch data
    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Convert rows into a list of dictionaries
        table_data = [dict(zip(column_names, row)) for row in rows]
        database_data[table_name] = table_data

    # Write the data to a JSON file
    # output_file = 'database.json'  # Specify the JSON file name
    #with open(output_file, 'w', encoding='utf-8') as json_file:
    json_data = json.dumps(database_data, indent=4)

    # Close the connection
    connection.close()

    return json_data