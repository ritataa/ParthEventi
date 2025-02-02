import sqlite3
import os

def create_database():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(ROOT_DIR, 'db', 'database.db')
    
    # Elimina il file del database se esiste
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(os.path.join(ROOT_DIR, 'db', 'login.sql'), 'r') as sql_file:
        sql_script = sql_file.read()
    
    cursor.executescript(sql_script)
    
    # Verifica che la tabella sia stata creata correttamente
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='utenti_registrati';")
    table_exists = cursor.fetchone()
    
    # Verifica il contenuto della tabella per debug
    cursor.execute("SELECT * FROM utenti_registrati")
    all_users = cursor.fetchall()
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()