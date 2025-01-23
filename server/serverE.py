import json
import os
from PyQt5.QtWidgets import QMessageBox, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from common.communication import loadJSONFromFile, request_constructor_str

def main():
    import socket
    import json
    from threading import Thread

    # Carica la configurazione del server
    ROOT_DIR = os.path.abspath(os.curdir)
    server_coords = loadJSONFromFile(os.path.join(ROOT_DIR, "server_address.json"))
    
    
    # Crea un socket per il server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_coords)
    server_socket.listen(5)
    
    print(f"Server in ascolto su {server_coords[0]}:{server_coords[1]}")

    def handle_client(client_socket):
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Richiesta ricevuta: {request}")
        
        # Logica per gestire le richieste dei client
        # (Registrazione, verifica validità, attivazione/sospensione accesso)
        
        response = "Richiesta elaborata"
        client_socket.send(response.encode('utf-8'))
        client_socket.close()

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connessione da {addr}")
        client_handler = Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()