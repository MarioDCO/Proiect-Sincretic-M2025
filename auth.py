# partea de autentificare: inregistrare si login

import json
import hashlib # biblioteca pentru ascunderea parolelor
import os

USERS_FILE = 'users.json' 

def _hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def _load_users():
    # citeste fisierul json daca exista un cont deja creat
    if not os.path.exists(USERS_FILE):
        return {} 
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {} 

def _save_users(users):
    # scrie in fisierul json
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    # functia de inregistrare.
    if not username or not password:
        return (False, "numele de utilizator si parola nu pot fi goale.")

    users = _load_users()

    # verifica daca numele e deja folosit
    if username in users:
        return (False, "eroare: numele de utilizator este deja folosit!") 
    
    # daca e bun, ascunde parola si salveaza noul cont
    users[username] = _hash_password(password)
    _save_users(users)
    return (True, f"succes! contul '{username}' a fost creat.")

def login_user(username, password):
    # functia de login.
    if not username or not password:
        return (False, "te rog introdu numele de utilizator si parola.") 
        
    users = _load_users()

    # verifica daca utilizatorul exista
    if username not in users:
        return (False, "eroare: nume de utilizator inexistent.") 

    # ascunde parola data de utilizator si o compara cu cea ascunsa din fisierul .json
    hashed_password = users[username]
    if hashed_password == _hash_password(password):
        return (True, username)
    else:
        return (False, "eroare: parola incorecta.")