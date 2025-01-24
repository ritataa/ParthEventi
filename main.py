# Contenuto di main.py

import json
import os

def load_server_config():
    with open('server_address.json') as config_file:
        return json.load(config_file)

def start_client(client_file):
    os.system(f"python {client_file}")

if __name__ == "__main__":
    config = load_server_config()
    address = config['address']
    port = config['port']
    
    print("Seleziona un'opzione:")
    print("1. Registrazione Partecipante")
    print("2. Verifica Validità Tessere")
    print("3. Sospensione/Attivazione Accesso")
    
    choice = input("Inserisci il numero dell'opzione: ")
    
    if choice == "1":
        start_client("client/client.py")
    elif choice == "2":
        start_client("client/clientC.py")
    elif choice == "3":
        start_client("client/clientO.py")
    else:
        print("Opzione non valida")