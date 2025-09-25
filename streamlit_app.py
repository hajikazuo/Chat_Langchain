import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv() 
API_URL = os.getenv("API_URL", "http://localhost:5555")

def api_post(endpoint, payload, token=None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    res = requests.post(f"{API_URL}{endpoint}", json=payload, headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        st.error(f"Erro {res.status_code}: {res.text}")
        return None

def api_get(endpoint, token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_URL}{endpoint}", headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        st.error(f"Erro {res.status_code}: {res.text}")
        return None
    
def main():
    st.set_page_config(page_title="Assistente Educação Financeira", page_icon="💰")
    st.title("💰 Assistente Educação Financeira")

    if "token" not in st.session_state:
        st.session_state.token = None

    if not st.session_state.token:
        tab1, tab2 = st.tabs(["Login", "Registrar"])

        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Senha", type="password", key="login_password")
            if st.button("Entrar"):
                resp = api_post("/login", {"email": email, "password": password})
                if resp and resp.get("access_token"):
                    st.session_state.token = resp["access_token"]
                    st.session_state.email = email
                    st.success("Login realizado com sucesso!")

                    st.switch_page("pages/chat_page.py")

        with tab2:
            email_r = st.text_input("Email", key="reg_email")
            password_r = st.text_input("Senha", type="password", key="reg_password")
            if st.button("Registrar"):
                resp = api_post("/register", {"email": email_r, "password": password_r})
                if resp:
                    st.success("Registrado com sucesso! Faça login agora.")
    else:
        st.switch_page("pages/chat_page.py")

if __name__ == "__main__":
    main()

