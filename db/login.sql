CREATE TABLE utenti_registrati (
    id_utente INT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cognome VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    data_registrazione DATE DEFAULT CURRENT_DATE,
    data_validita DATE NOT NULL
);
