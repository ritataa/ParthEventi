# Contenuto del file client/client.py

import requests

SERVER_ADDRESS = "http://127.0.0.1:9000"

def register_participant(name, email):
    payload = {
        "name": name,
        "email": email
    }
    response = requests.post(f"{SERVER_ADDRESS}/register", json=payload)
    return response.json()

def main():
    print("Registrazione Partecipante")
    name = input("Inserisci il tuo nome: ")
    email = input("Inserisci la tua email: ")
    
    result = register_participant(name, email)
    print("Risultato della registrazione:", result)

if __name__ == "__main__":
    main()