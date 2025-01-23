def activate_access(participant_id):
    # Logica per attivare l'accesso per un partecipante
    pass

def suspend_access(participant_id):
    # Logica per sospendere l'accesso per un partecipante
    pass

def main():
    # Interfaccia utente per attivare o sospendere l'accesso
    print("Gestione Accesso Partecipanti")
    print("1. Attivare Accesso")
    print("2. Sospendere Accesso")
    
    choice = input("Seleziona un'opzione: ")
    participant_id = input("Inserisci l'ID del partecipante: ")
    
    if choice == '1':
        activate_access(participant_id)
        print(f"Accesso attivato per il partecipante {participant_id}.")
    elif choice == '2':
        suspend_access(participant_id)
        print(f"Accesso sospeso per il partecipante {participant_id}.")
    else:
        print("Opzione non valida.")

if __name__ == "__main__":
    main()