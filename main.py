# Contenuto di main.py

import json
from server.serverE import start_server

def load_server_config():
    with open('server_address.json') as config_file:
        return json.load(config_file)

if __name__ == "__main__":
    config = load_server_config()
    address = config['server']['address']
    port = config['server']['port']
    
    start_server(address, port)