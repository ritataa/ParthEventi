# Progetto di Gestione delle Tessere di Accesso agli Eventi

## Traccia
Creare un sistema per la gestione di tessere di accesso a eventi. Un partecipante si registra utilizzando un client, che comunica con un ente organizzatore. L'ente invia i dettagli al ServerE, che gestisce le tessere e il periodo di validità.
Un ClientC consente di verificare la validità delle tessere. Un ClientO consente di sospendere o attivare l'accesso per un partecipante.


## Descrizione
Questo progetto ha lo scopo di gestire le tessere di accesso per vari eventi. Include funzionalità per creare, aggiornare, eliminare e visualizzare le tessere di accesso.

## Struttura del Progetto
- `client/`: Contiene i file del client per la registrazione, la verifica e la gestione delle tessere.
  - `client.py`: Logica principale del client per la registrazione dei partecipanti.
  - `clientO.py`: Funzionalità per sospendere o attivare l'accesso per un partecipante.
  - `clientC.py`: Funzionalità per controllare la validità delle tessere di accesso.
  
- `server/`: Contiene il file del server per gestire le richieste dei client.
  - `serverE.py`: Logica principale del server per gestire le tessere e le richieste dei client.

- `db/`: Directory per i file relativi al database, come la gestione della connessione e i modelli di dati.

- `main.py`: Punto di ingresso dell'applicazione, inizializza il server e ascolta le richieste in arrivo.

- `server_address.json`: Configurazione del server, inclusi indirizzo, numero di porta e durata di validità delle tessere.

- `requirements.txt`: Elenco delle dipendenze necessarie per il progetto, come PyQt5 e PyQt6.

## Istruzioni per l'Installazione
1. Clona il repository:
    ```sh
    git clone <repository_url>
    ```
2. Naviga nella directory del progetto:
    ```sh
    cd gestione-tessere-eventi
    ```
3. Installa le dipendenze:
    ```sh
    pip install -r requirements.txt
    ```

## Utilizzo
Esegui il file `main.py` per avviare l'applicazione:
```sh
python main.py
```