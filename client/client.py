import requests
import json
import os
import re
import sqlite3
import sys
import random

from PyQt5.QtWidgets import QMessageBox, QDialog, QHBoxLayout, QLabel, QPushButton

# Aggiungi il percorso del modulo SelMultiplexClient.py al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SelMultiplexClient import launchMethod
from common.communication import request_constructor_str, loadJSONFromFile

# Imposta il percorso del database relativo alla posizione di questo script
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, '..', 'db', 'database.db')
print(f"Percorso del database: {DB_PATH}")  # Aggiungi questa riga per il debug

server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "..", "server_address.json"))
SERVER_ADDRESS = server_coords['address']
SERVER_PORT = server_coords['port']

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utenti_registrati (
            id_utente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cognome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            data_registrazione DATE DEFAULT CURRENT_DATE,
            data_validita DATE NOT NULL,
            id_tessera TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def generate_card_id():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    while True:
        card_id = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        cursor.execute("SELECT * FROM utenti_registrati WHERE id_tessera = ?", (card_id,))
        if not cursor.fetchone():
            break
    conn.close()
    return card_id

def register_participant(name, surname, email, password):
    card_id = generate_card_id()
    payload = {
        "name": name,
        "surname": surname,
        "email": email,
        "password": password,
        "card_id": card_id
    }
    request_data = request_constructor_str(payload, "register")
    print(f"Request data: {request_data}")  # Aggiungi questa riga per il debug
    response = launchMethod(request_data, SERVER_ADDRESS, SERVER_PORT)
    print(f"Risposta dal server: {response}")  # Aggiungi questa riga per il debug
    if not response:
        print("Errore: Risposta vuota dal server")
        return {"status": "error", "message": "Risposta vuota dal server"}, card_id
    return json.loads(response), card_id

def save_credentials_to_db(name, surname, email, password, card_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Inserisci il nuovo utente senza verificare se esiste già
        cursor.execute("""
        INSERT INTO utenti_registrati (nome, cognome, email, password, data_validita, id_tessera)
        VALUES (?, ?, ?, ?, DATE('now', '+1 year'), ?)
        """, (name, surname, email, password, card_id))
        
        conn.commit()
        print(f"Utente {email} registrato con successo nel database locale")
    except sqlite3.IntegrityError as e:
        print(f"Errore di integrità del database: {e}")
    finally:
        conn.close()

def main():
    init_db()
    print("Registrazione Partecipante")
    name = input("Inserisci il tuo nome: ")
    surname = input("Inserisci il tuo cognome: ")
    email = input("Inserisci la tua email: ")
    password = input("Inserisci la tua password: ")
    
    result, card_id = register_participant(name, surname, email, password)
    print("Risultato della registrazione:", result)
    
    if result["status"] == "success":
        save_credentials_to_db(name, surname, email, password, card_id)
        print(f"Registrazione completata con successo. Il tuo ID tessera è: {card_id}")
    else:
        print(f"Errore nella registrazione: {result['message']}")

if __name__ == "__main__":
    main()