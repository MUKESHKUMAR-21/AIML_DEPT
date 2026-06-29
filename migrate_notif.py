import sqlite3
import os

db_path = os.path.join('instance', 'aiml.db')
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE notification ADD COLUMN category VARCHAR(50) DEFAULT 'general'")
        conn.commit()
        print("Successfully added 'category' column to notification table.")
    except sqlite3.OperationalError as e:
        print(f"Migration error (column might already exist): {e}")
    conn.close()
else:
    print(f"Database not found at {db_path}")
