import sqlite3
import os

ROOT_DIR = os.path.abspath(os.curdir)
DB_PATH = os.path.join(ROOT_DIR, 'db', 'database.db')

def view_registered_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM utenti_registrati")
    rows = cursor.fetchall()
    
    if rows:
        print("Utenti registrati:")
        for row in rows:
            print(row)
    else:
        print("Nessun utente registrato trovato.")
    
    conn.close()

if __name__ == "__main__":
    view_registered_users()