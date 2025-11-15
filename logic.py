# logic.py
# (versiune 3.7.2 - corectat bug-urile 'valueerror', 'exception' si 'none')

import json
import os
import config 
from datetime import datetime, date 

CUSTOM_KEYWORDS_FILE = "custom_keywords.json" # "memoria" ai-ului

def filter_expenses_by_date(expenses_list, start_date, end_date):
    # primeste lista completa de cheltuieli si o perioada
    # si returneaza o lista noua, mai mica, doar cu cheltuielile
    # din acea perioada.
    filtered_list = []
    for expense in expenses_list:
        expense_date_str = expense.get('date') 
        if not expense_date_str:
            continue
        try:
            expense_date = date.fromisoformat(expense_date_str)
            # verifica daca data cheltuielii este intre cele doua date
            if start_date <= expense_date <= end_date:
                filtered_list.append(expense)
        except ValueError: # <-- CORECTAT (era 'valueerror')
            print(f"ignorat format data invalid: {expense_date_str}")
    return filtered_list

# --- sectiunea de invatare a ai-ului ---

def _load_custom_keywords():
    # citeste fisierul-memorie `custom_keywords.json`
    if not os.path.exists(CUSTOM_KEYWORDS_FILE):
        return {}
    try:
        with open(CUSTOM_KEYWORDS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, TypeError): 
        return {}

def _save_custom_keywords(keywords):
    # scrie in fisierul-memorie `custom_keywords.json`
    with open(CUSTOM_KEYWORDS_FILE, 'w') as f:
        json.dump(keywords, f, indent=4)

def learn_new_keyword(keyword, new_category):
    # functia de invatare, chemata de interfata.
    # primeste un singur cuvant (ex: "netflix") si o categorie
    # si le adauga in fisierul-memorie.
    try:
        keyword = keyword.lower().strip() 
        if len(keyword) <= 2:
            return # ignora cuvinte prea scurte
        keywords_db = _load_custom_keywords()
        if new_category not in keywords_db:
            keywords_db[new_category] = []
        if keyword not in keywords_db[new_category]:
            keywords_db[new_category].append(keyword)
            _save_custom_keywords(keywords_db)
            print(f"am invatat: {keyword} -> {new_category}")
    except Exception as e: # <-- CORECTAT (era 'exception')
        print(f"eroare la invatare: {e}")

# --- functiile de logica si calcul ---

def classify_expense(descriere):
    # functia centrala a ai-ului, care decide categoria.
    descriere_mica = descriere.lower()
    
    # 1. cauta intai in memoria invatata (`custom_keywords.json`)
    custom_keywords = _load_custom_keywords()
    for categorie, cuvinte_cheie in custom_keywords.items():
        for cuvant in cuvinte_cheie:
            if cuvant in descriere_mica:
                return categorie 

    # 2. daca nu gaseste, cauta in regulile de baza (`config.py`)
    for categorie, cuvinte_cheie in config.CATEGORII_CHEIE.items():
        for cuvant in cuvinte_cheie:
            if cuvant in descriere_mica:
                return categorie
                
    # 3. daca tot nu gaseste, returneaza "diverse"
    return "diverse"

def calculate_totals(cheltuieli):
    # un calculator simplu.
    totaluri = {}
    for item in cheltuieli:
        categorie = item["categorie"]
        pret = item["pret"]
        totaluri[categorie] = totaluri.get(categorie, 0) + pret
    return totaluri

def check_budget(categorie, total_nou, total_anterior, user_budgets):
    # "gardianul" bugetului.
    buget_categorie = user_budgets.get(categorie, 0)
    
    if buget_categorie == 0:
        return None # <-- CORECTAT (era 'none')

    # 1. verifica daca a depasit bugetul
    if total_nou > buget_categorie and total_anterior <= buget_categorie:
        depasire = total_nou - buget_categorie
        return f"⚠️ atentie: tocmai ai depasit bugetul pentru '{categorie}'! esti peste cu {depasire:.2f} ron."
    
    # 2. verifica daca a intrat in "zona rosie" (sub 50 ron ramasi)
    bani_ramasi = buget_categorie - total_nou
    if total_nou <= buget_categorie and bani_ramasi <= 50:
        if (buget_categorie - total_anterior) > 50:
             return f"ℹ️ nota: esti aproape de limita! mai ai doar {bani_ramasi:.2f} ron din bugetul pentru '{categorie}'."
    
    return None # <-- CORECTAT (era 'none')

def get_summary(totaluri, monthly_income, user_budgets):
    # "contabilul" care scrie raportul text.
    
    summary_string = "--- rezumat financiar (cu bugete) ---\n\n"
    total_general = 0
    for categorie, total in totaluri.items():
        total_general += total
        buget_cat = user_budgets.get(categorie, 0)
        
        if buget_cat > 0:
            ramas = buget_cat - total
            if ramas >= 0:
                summary_string += f"total {categorie}: {total:.2f} ron (buget: {buget_cat:.2f} ron, ramas: {ramas:.2f} ron)\n"
            else:
                summary_string += f"total {categorie}: {total:.2f} ron (buget: {buget_cat:.2f} ron, depasit cu: {abs(ramas):.2f} ron) 🔴\n"
        else:
            summary_string += f"total {categorie}: {total:.2f} ron (fara buget setat)\n"
    
    summary_string += "---------------------------------------\n"
    bani_ramasi = monthly_income - total_general
    summary_string += f"venit lunar setat: {monthly_income:.2f} ron\n"
    summary_string += f"total cheltuit (in perioada filtrata): {total_general:.2f} ron\n"
    summary_string += "=======================================\n"
    summary_string += f"bani ramasi (din venitul total): {bani_ramasi:.2f} ron\n"
    
    return summary_string