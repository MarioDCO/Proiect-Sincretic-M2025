# Asistent Financiar AI cu Streamlit

Acesta este un proiect pentru școală ce prezintă o aplicație web completă pentru gestionarea bugetului personal. Aplicația este construită în Python și Streamlit și include un sistem de autentificare securizat, un motor AI de clasificare a cheltuielilor și management avansat al bugetului.

---

## 📸 Screenshots

*(Aici vei adăuga tu screenshot-urile. Cel mai simplu mod este să faci pozele, să le tragi (drag & drop) direct în acest fișier text pe site-ul GitHub, iar el va genera link-ul automat pentru tine.)*

**Ecranul de Login și Register:**
![Ecran Login](https://github.com/user-attachments/assets/e9c283c3-d814-43cc-a20f-f9a57fe5daff)

**Dashboard-ul Principal:**
![Dashboard](https://github.com/user-attachments/assets/7bc29a9c-4b77-48b8-afbf-279a8552d7b5)

**Interfata de filtrare/buget/situatie financiara curenta:**
![Interfata](https://github.com/user-attachments/assets/57e3a92f-94dc-4092-9d7f-6ff51eba92ca)

**Distribuia cheltuielilor/vizionare istoric/stergere greseli:**
![Grafic/Istoric](https://github.com/user-attachments/assets/354b986a-30a2-4792-9143-21a5ece95390)

## 💡 Funcționalități Cheie

* **Sistem de Autentificare:** Login și Register cu parole securizate (hashed).
* **Management per Utilizator:** Fiecare utilizator are propriile cheltuieli, venituri și bugete, salvate în fișiere `.json` separate.
* **Motor AI de Învățare:** Clasifică automat cheltuielile folosind reguli de bază și o "memorie" (`custom_keywords.json`) care se îmbogățește.
* **Formular de Învățare:** Când AI-ul nu știe o categorie, te întreabă pe tine și învață un cuvânt cheie nou pentru viitor.
* **Management Buget:** Permite utilizatorului să își seteze venitul lunar total și bugete personalizate pentru fiecare categorie în parte.
* **Notificări Inteligente:** Ești avertizat direct în interfață când mai ai sub 50 RON rămași într-o categorie de buget.
* **Filtrare pe Bază de Dată:** Permite analiza cheltuielilor folosind un selector de calendar (ex: 'Luna aceasta', 'Ultimele 7 zile', etc.).
* **Managementul Tranzacțiilor:** Poți adăuga cheltuieli noi (cu dată) și poți șterge tranzacțiile adăugate greșit.
* **Vizualizare Date:** Un grafic circular (Pie Chart) interactiv, construit cu Plotly, arată distribuția cheltuielilor pentru perioada selectată.
* **Temă Personalizată:** Include o temă "Interstellar" (Dark Mode) și un comutator pentru "White Mode".

---