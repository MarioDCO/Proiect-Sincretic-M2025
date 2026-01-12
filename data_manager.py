# data_manager.py
# se ocupa de citirea si scrierea fisierelor json cu cheltuieli.

import json
import os

DATA_FOLDER = "data" 

def _get_user_filepath(username):
    """returneaza calea catre fisierul de date al utilizatorului."""
    return os.path.join(DATA_FOLDER, f"{username}.json")

def _ensure_data_folder():
    """se asigura ca folderul 'data/' exista. daca nu, il creeaza."""
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

def load_finances(username):
    """
    incarca datele unui utilizator (venit + cheltuieli).
    returneaza un dictionar, de ex: {'monthly_income': 5000.0, 'expenses': [...]}
    """
    _ensure_data_folder()
    filepath = _get_user_filepath(username)
    
    # structura de baza pe care o returnam daca nu exista fisier
    default_data = {"monthly_income": 0.0, "expenses": []} 

    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                print("Detectat format vechi de date. Se converteste...")
                default_data["expenses"] = data
                return default_data
            
           
            if "monthly_income" not in data:
                data["monthly_income"] = 0.0
            if "expenses" not in data:
                data["expenses"] = []
                
            return data

        except json.JSONDecodeError:
            return default_data 
    
    return default_data 

def save_finances(username, user_data):
    """
    salveaza intregul obiect de date al utilizatorului (venit + cheltuieli).
    user_data este acum un dictionar.
    """
    _ensure_data_folder()
    filepath = _get_user_filepath(username)
    
    with open(filepath, 'w') as f:
        json.dump(user_data, f, indent=4)