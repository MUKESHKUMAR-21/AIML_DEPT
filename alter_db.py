import sqlite3

def alter_db():
    conn = sqlite3.connect('instance/aiml.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE student_credentials ADD COLUMN section VARCHAR(10) DEFAULT 'A'")
        conn.commit()
        print("Column 'section' added successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    alter_db()
