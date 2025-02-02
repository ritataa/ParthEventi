import sqlite3
import json
import os

# Imposta il percorso del database relativo alla posizione di questo script
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, 'db', 'database.db')

def method_switch(header, payload):
    if header == "register":
        return register_user(payload)
    elif header == "validate":
        return validate_user(payload)
    elif header == "suspend":
        return suspend_user(payload)
    elif header == "activate":
        return activate_user(payload)
    else:
        return {"status": "error", "message": "Invalid header"}

def register_user(payload):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Verifica il contenuto del database per debug
        cursor.execute("SELECT * FROM utenti_registrati")
        all_users = cursor.fetchall()
        print("Utenti attualmente registrati:", all_users)
        
        # Verifica se l'utente esiste già
        cursor.execute("SELECT * FROM utenti_registrati WHERE email = ?", (payload['email'],))
        user = cursor.fetchone()
        if user:
            print(f"Errore: L'utente con email {payload['email']} esiste già")
            return {"status": "error", "message": "User already exists"}
        
        # Verifica se l'ID tessera esiste già
        cursor.execute("SELECT * FROM utenti_registrati WHERE id_tessera = ?", (payload['card_id'],))
        card = cursor.fetchone()
        if card:
            print(f"Errore: L'ID tessera {payload['card_id']} esiste già")
            return {"status": "error", "message": "Card ID already exists"}
        
        # Inserisci il nuovo utente
        cursor.execute("""
        INSERT INTO utenti_registrati (nome, cognome, email, password, data_validita, id_tessera, isAttivo)
        VALUES (?, ?, ?, ?, DATE('now', '+1 year'), ?, 1)
        """, (payload['name'], payload['surname'], payload['email'], payload['password'], payload['card_id']))
        
        conn.commit()
        print(f"Utente {payload['email']} registrato con successo")
        return {"status": "success", "message": "User registered successfully"}
    except sqlite3.IntegrityError as e:
        print(f"Errore di integrità del database: {e}")
        return {"status": "error", "message": "Database integrity error"}
    finally:
        conn.close()

def validate_user(payload):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM utenti_registrati WHERE id_tessera = ? AND isAttivo = 1", (payload['card_id'],))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"status": "success", "message": "Tessera valida", "data_validita": user[6]}
    else:
        return {"status": "error", "message": "Tessera non trovata o utente non attivo"}

def suspend_user(payload):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE utenti_registrati SET isAttivo = 0 WHERE email = ?", (payload['email'],))
    conn.commit()
    
    # Verifica il contenuto del database per debug
    cursor.execute("SELECT * FROM utenti_registrati")
    all_users = cursor.fetchall()
    print("Utenti attualmente registrati:", all_users)
    
    conn.close()
    
    return {"status": "success", "message": "Accesso sospeso"}

def activate_user(payload):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE utenti_registrati SET isAttivo = 1 WHERE email = ?", (payload['email'],))
    conn.commit()
    
    # Verifica il contenuto del database per debug
    cursor.execute("SELECT * FROM utenti_registrati")
    all_users = cursor.fetchall()
    print("Utenti attualmente registrati:", all_users)
    
    conn.close()
    
    return {"status": "success", "message": "Accesso attivato"}