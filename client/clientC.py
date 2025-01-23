import requests
import json

def check_ticket_validity(ticket_id):
    with open('../server_address.json') as config_file:
        config = json.load(config_file)
    
    server_address = config['server']['address']
    server_port = config['server']['port']
    url = f'http://{server_address}:{server_port}/check_ticket'

    response = requests.post(url, json={'ticket_id': ticket_id})

    if response.status_code == 200:
        result = response.json()
        if result['valid']:
            print(f"La tessera {ticket_id} è valida.")
        else:
            print(f"La tessera {ticket_id} non è valida.")
    else:
        print("Errore nella comunicazione con il server.")

if __name__ == "__main__":
    ticket_id = input("Inserisci l'ID della tessera da controllare: ")
    check_ticket_validity(ticket_id)