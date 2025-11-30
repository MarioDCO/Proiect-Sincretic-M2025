# Financial Assistant App (Python & Streamlit)

This is my project for the Python course. I built a personal finance application that helps users track their budget, income, and expenses. The main goal was to create an app that is not just a simple calculator, but one that can "learn" from the user's input.

---

## 📸 How it looks

**Login / Register:**
![Login Screen](https://github.com/user-attachments/assets/e9c283c3-d814-43cc-a20f-f9a57fe5daff)

<br>

**Main Dashboard & Charts:**
![Dashboard](https://github.com/user-attachments/assets/7bc29a9c-4b77-48b8-afbf-279a8552d7b5)

<br>

**Budget Settings:**
![Interface](https://github.com/user-attachments/assets/57e3a92f-94dc-4092-9d7f-6ff51eba92ca)

<br>

**Managing Expenses:**
![Chart/History](https://github.com/user-attachments/assets/354b986a-30a2-4792-9143-21a5ece95390)

<br>

---

## 🛠️ What the app does

I focused on creating a complete flow for the user:

1.  **Login System:** You can create an account and log in. The passwords are encrypted (hashed) for security, so they are not stored as plain text.
2.  **Data Persistence:** Every user has their own `.json` file. This means the data is saved even after you close the app.
3.  **Smart Classification:** This is the cool part. If you type "Netflix", the app might not know what it is initially. But if you tell it once that "Netflix" is "Utilities" or "Fun", it saves that word in a memory file (`custom_keywords.json`). Next time, it will auto-fill the category for you.
4.  **Budget Alerts:** I added a logic that checks your remaining budget. If you have less than 50 RON left in a category, it shows a warning message.
5.  **Visualization:** I used the `Plotly` library to generate a pie chart, so you can easily see where your money goes.
6.  **Filters:** You can select a specific date range (e.g., this month only) to see relevant data.

---

## 💻 How to run the project

If you want to run this on your local machine, here are the steps:

**1. Clone the repository**
```bash
git clone [https://github.com/MarioDCO/Proiect-Sincretic-M2025.git](https://github.com/MarioDCO/Proiect-Sincretic-M2025.git)
cd Asistent-Financiar-AI-Streamlit
##Project Structure

Asistent-Financiar-AI/
├── app_streamlit.py      # Main Application Entry Point (Frontend & UI)
├── logic.py              # The "Brain": Calculations, AI Logic, Filtering
├── auth.py               # Authentication Handler (Login/Register/Hashing)
├── data_manager.py       # File I/O: Reads/Writes JSON data
├── config.py             # Default Settings & Base Keywords
├── requirements.txt      # List of dependencies
├── .streamlit/           # Theme Configuration & Secrets
│   └── config.toml
├── data/                 # (Generated) User data files store here
└── assets/               # Images for README
---