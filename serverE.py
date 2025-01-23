import json
import os
from PyQt5.QtWidgets import QMessageBox, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
# Rimuovere l'importazione del modulo non trovato
# from common.communication import loadJSONFromFile, request_constructor_str
import socket
import json
from threading import Thread
import sqlite3  # Aggiungere l'importazione per sqlite3

def loadJSONFromFile(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def main():
    import socket
    import json
    from threading import Thread

    # Carica la configurazione del server
    ROOT_DIR = os.path.abspath(os.curdir)
    server_config = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
    
    # Verifica che le chiavi "address" e "port" esistano
    if "server" not in server_config or "address" not in server_config["server"] or "port" not in server_config["server"]:
        raise KeyError("La configurazione del server deve contenere le chiavi 'address' e 'port'")
    
    server_coords = (server_config["server"]["address"], server_config["server"]["port"])
    
    # Crea un socket per il server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_coords)
    server_socket.listen(5)
    
    print(f"Server in ascolto su {server_coords[0]}:{server_coords[1]}")

    def handle_client(client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Richiesta ricevuta: {request}")
        
        # Parsing della richiesta JSON
        request_data = json.loads(request)
        action = request_data.get("action")
        
        if action == "register":
            nome = request_data.get("nome")
            cognome = request_data.get("cognome")
            email = request_data.get("email")
            password = request_data.get("password")
            
            # Connessione al database
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Inserimento dell'utente nel database
            cursor.execute("""
                INSERT INTO utenti_registrati (nome, cognome, email, password)
                VALUES (?, ?, ?, ?)
            """, (nome, cognome, email, password))
            
            conn.commit()
            conn.close()
            
            response = {"status": "success", "message": "Registrazione completata"}
        else:
            response = {"status": "error", "message": "Azione non riconosciuta"}
        
        client_socket.send(json.dumps(response).encode('utf-8'))
        client_socket.close()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connessione da {addr}")
        client_handler = Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()