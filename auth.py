# auth.py
# acest fisier este "paznicul". se ocupa doar de login si register.

import json
import hashlib # biblioteca pentru criptarea (ascunderea) parolelor
import os

USERS_FILE = 'users.json' # fisierul cu baza de date de conturi

def _hash_password(password):
    # functia care "ascunde" parola.
    # nu salvam niciodata parola reala, doar acest "hash".
    return hashlib.sha256(password.encode()).hexdigest()

def _load_users():
    # citeste fisierul `users.json`
    if not os.path.exists(USERS_FILE):
        return {} 
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} 

def _save_users(users):
    # scrie in fisierul `users.json`
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    # functia de inregistrare.
    # primeste datele de la interfata.
    
    if not username or not password:
        return (False, "numele de utilizator si parola nu pot fi goale.") # <-- CORECTAT

    users = _load_users()

    # verifica daca numele e deja folosit
    if username in users:
        return (False, "eroare: numele de utilizator este deja folosit!") # <-- CORECTAT
    
    # daca e ok, ascunde parola si salveaza noul cont
    users[username] = _hash_password(password)
    _save_users(users)
    return (True, f"succes! contul '{username}' a fost creat.") # <-- CORECTAT

def login_user(username, password):
    # functia de login.
    # primeste datele de la interfata.
    
    if not username or not password:
        return (False, "te rog introdu numele de utilizator si parola.") # <-- CORECTAT
        
    users = _load_users()

    # verifica daca utilizatorul exista
    if username not in users:
        return (False, "eroare: nume de utilizator inexistent.") # <-- CORECTAT

    # ascunde parola data de utilizator si o compara cu cea
    # ascunsa din fisierul .json
    hashed_password = users[username]
    if hashed_password == _hash_password(password):
        return (True, username) # succes! # <-- CORECTAT (aceasta e linia 65)
    else:
        return (False, "eroare: parola incorecta.") # <-- CORECTAT