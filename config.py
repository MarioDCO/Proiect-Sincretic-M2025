# config.py
# Panoul de control al aplicației.
# Aici stocăm regulile și setările.

# "Inteligența" AI - Baza de cunoștințe pentru clasificare
CATEGORII_CHEIE = {
    "Mancare/Supermarket": ["chips", "faina", "suc", "lapte", "paine", "apa", "supermarket", "magazin", "mancare", "legume", "fructe", "kaufland", "lidl", "mega", "piata"],
    "Utilitati": ["factura", "gaz", "curent", "apa", "intretinere", "chirie", "telefon", "digi", "vodafone"],
    "Transport": ["benzina", "motorina", "autobuz", "metrou", "tren", "bilet", "uber", "bolt", "motorina"],
    "Sanatate/Fitness": ["sala", "abonament sala", "medicamente", "doctor", "fitness", "farmacie", "pastile"],
    "Divertisment/Timp Liber": ["film", "cinema", "restaurant", "cafea", "bar", "concert", "iesire", "carte", "pizza"],
    "Shopping (Haine/Electronice)": ["haine", "pantofi", "bluza", "telefon", "gadget", "laptop", "emag", "cadou"]
}

# Setarea bugetelor lunare
BUGETE = {
    "Mancare/Supermarket": 1000,
    "Utilitati": 700,
    "Transport": 300,
    "Sanatate/Fitness": 200,
    "Divertisment/Timp Liber": 400,
    "Shopping (Haine/Electronice)": 500,
    "Diverse": 150
}