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
);