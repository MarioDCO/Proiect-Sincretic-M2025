
import streamlit as st
import auth  
import data_manager 
import logic 
import config 
import pandas as pd 
import plotly.express as px 
from datetime import datetime, date 

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = None
if 'pending_expense' not in st.session_state:
    st.session_state['pending_expense'] = None

# deseneaza pagina principala 
def show_login_page():
    # deseneaza pagina de login 
    st.title("bun venit la asistentul financiar")
    tab_login, tab_register = st.tabs(["🔒 autentificare (login)", "📝 inregistrare cont nou"])

    with tab_login:
        with st.form("login_form"):
            login_user = st.text_input("nume de utilizator", key="login_u")
            login_pass = st.text_input("parola", type="password", key="login_p")
            login_button = st.form_submit_button("intra in cont")
            if login_button:
                status, message = auth.login_user(login_user, login_pass)
                if status:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = message
                    st.session_state['pending_expense'] = None 
                    st.rerun() 
                else:
                    st.error(message) 
    # deseneaza pagina register
    with tab_register:
        with st.form("register_form"):
            reg_user = st.text_input("alege un nume de utilizator", key="reg_u")
            reg_pass = st.text_input("alege o parola", type="password", key="reg_p")
            register_button = st.form_submit_button("inregistreaza-te")
            if register_button:
                status, message = auth.register_user(reg_user, reg_pass)
                if status:
                    st.success(message) 
                else:
                    st.error(message)

def handle_learning_form(user_data):
    # deseneaza formularul special de invatare
    lista_cheltuieli = user_data["expenses"]
    user_budgets = user_data.get("user_budgets", {})
    pending = st.session_state['pending_expense']
    descriere = pending['descriere']
    pret = pending['pret']
    data_cheltuielii = pending['date'] # data este deja un string din pasul anterior
    
    st.warning(f"🧠 timp sa invat! nu stiu unde sa incadrez: **'{descriere}'**")
    
    with st.form("learning_form"):
        st.write("ajuta-ma sa invat pentru viitor.")
        
        sugestie_cuvant = descriere.split()[0].lower()
        keyword_to_learn = st.text_input("ce cuvant cheie vrei sa invat din aceasta descriere?", 
                                         value=sugestie_cuvant)
        
        lista_categorii = list(config.CATEGORII_CHEIE.keys())
        if "diverse" not in lista_categorii:
            lista_categorii.append("diverse")
        new_category = st.selectbox("in ce categorie sa il pun?", options=lista_categorii)
        
        col1, col2 = st.columns(2)
        with col1:
            confirm_button = st.form_submit_button("✅ confirma si invata")
        with col2:
            cancel_button = st.form_submit_button("❌ anuleaza")

    if confirm_button:
        if keyword_to_learn:
            logic.learn_new_keyword(keyword_to_learn, new_category)
        else:
            st.error("nu ai specificat un cuvant cheie de invatat.")
            return 
        
        cheltuiala_corectata = {
            "id": datetime.now().timestamp(), 
            "date": data_cheltuielii, 
            "descriere": descriere,
            "pret": pret,
            "categorie": new_category 
        }
        user_data["expenses"].append(cheltuiala_corectata)
        
        totaluri_curente = logic.calculate_totals(lista_cheltuieli)
        total_anterior = totaluri_curente.get(new_category, 0) - pret 
        total_nou = totaluri_curente.get(new_category, 0)
        mesaj_buget = logic.check_budget(new_category, total_nou, total_anterior, user_budgets)
        
        data_manager.save_finances(st.session_state['username'], user_data)
        st.success(f"perfect! am invatat '{keyword_to_learn}' si am salvat cheltuiala.")
        
        if mesaj_buget:
            st.warning(mesaj_buget) 
            
        st.session_state['pending_expense'] = None 
        st.rerun()

    if cancel_button:
        st.info(f"ok, am anulat adaugarea pentru '{descriere}'.")
        st.session_state['pending_expense'] = None 
        st.rerun()

def handle_expense_form(user_data):
    # deseneaza formularul de adaugat cheltuieli.
    lista_cheltuieli = user_data["expenses"] 
    user_budgets = user_data.get("user_budgets", {})
    
    with st.form("expense_form", clear_on_submit=True):
        data_cheltuielii = st.date_input("data cheltuielii", value=datetime.now())
        descriere = st.text_input("ce ai cumparat?")
        pret = st.number_input("cat a costat? (ron)", min_value=0.0, format="%.2f")
        submit_expense = st.form_submit_button("adauga cheltuiala")

        if submit_expense and descriere:
            categorie_gasita = logic.classify_expense(descriere)
            
            cheltuiala = {
                "id": datetime.now().timestamp(), 
                "date": data_cheltuielii.strftime("%Y-%m-%d"), 
                "descriere": descriere,
                "pret": pret,
                "categorie": categorie_gasita
            }

            if categorie_gasita == "diverse":
                st.session_state['pending_expense'] = cheltuiala
                st.rerun() 
            else:
                totaluri_curente_toate = logic.calculate_totals(lista_cheltuieli)
                total_anterior = totaluri_curente_toate.get(categorie_gasita, 0)
                
                user_data["expenses"].append(cheltuiala)
                data_manager.save_finances(st.session_state['username'], user_data)
                
                st.success(f"✅ adaugat: '{descriere}' -> categoria: {categorie_gasita}")
                
                total_nou = total_anterior + pret
                mesaj_buget = logic.check_budget(categorie_gasita, total_nou, total_anterior, user_budgets)
                
                if mesaj_buget:
                    st.warning(mesaj_buget)

def show_main_app():
    #functia care construieste pagina principala
    username = st.session_state['username']
    
    user_data = data_manager.load_finances(username)
    lista_cheltuieli = user_data["expenses"]
    monthly_income = user_data["monthly_income"]
    user_budgets = user_data.get("user_budgets", config.BUGETE.copy())

    # sidebar-ul cu setari si filtre
    st.sidebar.title(f"salut, {username}!")
    
    st.sidebar.divider()
    st.sidebar.subheader("filtreaza perioada")
    today = date.today()
    start_of_month = today.replace(day=1)
    start_date = st.sidebar.date_input("data de inceput", value=start_of_month)
    end_date = st.sidebar.date_input("data de sfarsit", value=today)
    
    st.sidebar.divider() 
    
    st.sidebar.subheader("setari buget general")
    new_income = st.sidebar.number_input("seteaza venitul lunar total (ron)", 
                                         value=monthly_income, 
                                         min_value=0.0, 
                                         format="%.2f",
                                         key="income_input")
    
    if st.sidebar.button("salveaza venitul"):
        user_data["monthly_income"] = new_income
        data_manager.save_finances(username, user_data)
        st.sidebar.success("venit salvat!")
        st.rerun() 
        
    with st.sidebar.expander("📊 gestioneaza bugetele categoriilor"):
        bugete_modificate = user_budgets.copy()
        
        with st.form("budget_form"):
            toate_categoriile = list(config.CATEGORII_CHEIE.keys())
            if "diverse" not in toate_categoriile:
                toate_categoriile.append("diverse")
                
            for categorie in toate_categoriile:
                valoare_curenta = bugete_modificate.get(categorie, 0.0)
                bugete_modificate[categorie] = st.number_input(f"buget {categorie}", 
                                                               value=float(valoare_curenta), 
                                                               min_value=0.0, 
                                                               format="%.2f", 
                                                               key=f"budget_{categorie}")

            submitted = st.form_submit_button("salveaza bugetele categoriilor")

        if submitted:
            user_data['user_budgets'] = bugete_modificate 
            data_manager.save_finances(username, user_data) 
            st.success("bugetele pe categorii au fost actualizate!")
            st.rerun()

    st.sidebar.divider() 

    st.sidebar.subheader("situatia curenta")
    cheltuieli_filtrate = logic.filter_expenses_by_date(lista_cheltuieli, start_date, end_date)
    totaluri_curente = logic.calculate_totals(cheltuieli_filtrate) 
    total_general_cheltuit = sum(totaluri_curente.values())
    bani_ramasi = new_income - total_general_cheltuit 
    
    st.sidebar.metric("bani ramasi (din venit)", 
                      f"{bani_ramasi:.2f} ron", 
                      delta=f"-{total_general_cheltuit:.2f} ron cheltuiti (in perioada)",
                      delta_color="inverse") 

    st.sidebar.divider()
    if st.sidebar.button("logout (iesire)"):
        st.session_state['logged_in'] = False 
        st.session_state['username'] = None 
        st.session_state['pending_expense'] = None 
        st.rerun() 

    #incepe constructia paginii principale
    st.title("📈 Asistentul tau Financiar")
    st.info(f"afiseaza datele intre {start_date.strftime('%d-%m-%Y')} si {end_date.strftime('%d-%m-%Y')}")
    
    if st.session_state['pending_expense'] is None: 
        handle_expense_form(user_data)
    else:
        handle_learning_form(user_data)

    # rezumat (bazata pe datele filtrate)
    st.header("rezumatul cheltuielilor")
    if not cheltuieli_filtrate:
        st.info("nu ai nicio cheltuiala inregistrata pentru perioada selectata.")
    else:
        rezumat_text = logic.get_summary(totaluri_curente, new_income, user_budgets)
        st.text(rezumat_text) 
        
        st.subheader("distributia cheltuielilor (grafic)")
        if totaluri_curente:
            df_cheltuieli = pd.DataFrame(totaluri_curente.items(), columns=['categorie', 'suma'])
            fig = px.pie(df_cheltuieli, 
                         names='categorie', 
                         values='suma',
                         title='cheltuieli pe categorie (in perioada)',
                         color_discrete_sequence=px.colors.sequential.RdBu) 
            
            st.plotly_chart(fig, width='stretch') 
        
        with st.expander("vezi si gestioneaza tranzactiile filtrate"):
            st.write("aici poti sterge cheltuielile adaugate gresit. stergerea este permanenta.")
            
            col1, col2, col3, col4 = st.columns([2, 4, 2, 1])
            col1.text("data")
            col2.text("descriere")
            col3.text("suma")
            col4.text("actiune")
            st.divider()

            for expense in cheltuieli_filtrate:
                col1, col2, col3, col4 = st.columns([2, 4, 2, 1])
                col1.text(expense.get('date', 'n/a'))
                col2.text(expense.get('descriere', 'n/a'))
                col3.text(f"{expense.get('pret', 0):.2f} ron")
                
                id_cheltuiala = expense.get('id')
                if id_cheltuiala:
                    if col4.button("🗑️", key=id_cheltuiala, help="sterge aceasta cheltuiala"):
                        user_data["expenses"] = [
                            exp for exp in lista_cheltuieli 
                            if exp.get('id') != id_cheltuiala
                        ]
                        data_manager.save_finances(username, user_data)
                        st.success(f"am sters cheltuiala: '{expense.get('descriere')}'")
                        st.rerun()

#router-ul principal
if not st.session_state['logged_in']:
    show_login_page()
else:
    show_main_app()