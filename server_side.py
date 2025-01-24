import sqlite3
import json

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
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO utenti_registrati (nome, cognome, email, password, data_validita)
        VALUES (?, ?, ?, ?, DATE('now', '+1 year'))
        """, (payload['name'], payload['surname'], payload['email'], payload['password']))
        
        conn.commit()
        return {"status": "success", "message": "User registered successfully"}
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "User already exists"}
    finally:
        conn.close()

def validate_user(payload):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM utenti_registrati WHERE email = ?", (payload['email'],))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {"status": "success", "message": "Tessera valida", "data_validita": user[6]}
    else:
        return {"status": "error", "message": "Tessera non trovata"}

def suspend_user(payload):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("UPDATE utenti_registrati SET data_validita = DATE('now', '-1 day') WHERE email = ?", (payload['email'],))
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": "Accesso sospeso"}

def activate_user(payload):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    validity_duration = 30  # Durata di validità delle tessere in giorni
    
    cursor.execute("UPDATE utenti_registrati SET data_validita = DATE('now', ? || ' days') WHERE email = ?", (validity_duration, payload['email']))
    conn.commit()
    conn.close()
    
    return {"status": "success", "message": "Accesso attivato"}
