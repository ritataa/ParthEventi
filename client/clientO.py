import json
import os
import sqlite3
import sys

from PyQt5.QtWidgets import QMessageBox, QDialog, QHBoxLayout, QLabel, QPushButton

# Aggiungi il percorso del modulo SelMultiplexClient.py al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SelMultiplexClient import launchMethod
from common.communication import request_constructor_str, loadJSONFromFile

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(ROOT_DIR, '..', 'db', 'database.db')

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
            id_tessera TEXT NOT NULL UNIQUE,
            isAttivo INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

def suspend_user_access(email):
    payload = {
        "email": email
    }
    request_data = request_constructor_str(payload, "suspend")
    response = launchMethod(request_data, SERVER_ADDRESS, SERVER_PORT)
    return json.loads(response)

def activate_user_access(email):
    payload = {
        "email": email
    }
    request_data = request_constructor_str(payload, "activate")
    response = launchMethod(request_data, SERVER_ADDRESS, SERVER_PORT)
    return json.loads(response)

def main():
    init_db()
    print("Gestione Accesso Utenti")
    action = input("Vuoi sospendere o attivare l'accesso? (sospendere/attivare): ").strip().lower()
    email = input("Inserisci l'email dell'utente: ").strip()
    
    if action == "sospendere":
        result = suspend_user_access(email)
    elif action == "attivare":
        result = activate_user_access(email)
    else:
        print("Azione non valida.")
        return
    
    print("Risultato dell'operazione:", result)
    
    if result["status"] == "success":
        print(f"L'accesso per l'utente con email {email} è stato {action} con successo.")
    else:
        print(f"Errore nell'operazione: {result['message']}")

if __name__ == "__main__":
    main()