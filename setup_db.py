import sqlite3

def create_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    with open('db/login.sql', 'r') as sql_file:
        sql_script = sql_file.read()
    
    cursor.executescript(sql_script)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database e tabella creati con successo.")