# Contenuto del file client/client.py

import requests

SERVER_ADDRESS = "http://127.0.0.1:9000"

def register_participant(name, surname, email, password):
    payload = {
        "name": name,
        "surname": surname,
        "email": email,
        "password": password
    }
    response = requests.post(f"{SERVER_ADDRESS}/register", json=payload)
    return response.json()

def main():
    print("Registrazione Partecipante")
    name = input("Inserisci il tuo nome: ")
    surname = input("Inserisci il tuo cognome: ")
    email = input("Inserisci la tua email: ")
    password = input("Inserisci la tua password: ")
    
    result = register_participant(name, surname, email, password)
    print("Risultato della registrazione:", result)

if __name__ == "__main__":
    main()