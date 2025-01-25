# Contenuto del file client/client.py

import requests
import json
import os
import re
import sqlite3

from PyQt5.QtWidgets import QMessageBox, QDialog, QHBoxLayout, QLabel, QPushButton
# from pyqt5_plugins.examplebutton import QtWidgets

from SelMultiplexClient import launchMethod
from common.communication import request_constructor_str, loadJSONFromFile

ROOT_DIR = os.path.abspath(os.curdir)
DB_PATH = os.path.join(ROOT_DIR, 'db', 'database.db')

server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
SERVER_ADDRESS = server_coords['server']['address']
SERVER_PORT = server_coords['server']['port']


def register_participant(name, surname, email, password):
    payload = {
        "name": name,
        "surname": surname,
        "email": email,
        "password": password
    }
    request_data = request_constructor_str(payload, "register")
    response = launchMethod(request_data, SERVER_ADDRESS, SERVER_PORT)
    return json.loads(response)

def save_credentials_to_db(name, surname, email, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
        INSERT INTO utenti_registrati (nome, cognome, email, password, data_validita)
        VALUES (?, ?, ?, ?, DATE('now', '+1 year'))
        """, (name, surname, email, password))
        
        conn.commit()
    except sqlite3.IntegrityError:
        print("Errore: L'utente esiste già")
    finally:
        conn.close()

def main():
    print("Registrazione Partecipante")
    name = input("Inserisci il tuo nome: ")
    surname = input("Inserisci il tuo cognome: ")
    email = input("Inserisci la tua email: ")
    password = input("Inserisci la tua password: ")
    
    result = register_participant(name, surname, email, password)
    print("Risultato della registrazione:", result)
    
    if result["status"] == "success":
        save_credentials_to_db(name, surname, email, password)

if __name__ == "__main__":
    main()