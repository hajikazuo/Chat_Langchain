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
    st.set_page_config(page_title="Chat Financeiro", page_icon="💬")
    st.title("💬 Chat Financeiro")

    if "token" not in st.session_state or not st.session_state.token:
        st.warning("Por favor, faça login para acessar esta página.")
        st.switch_page("streamlit_app.py")

    st.caption(f"Logado como: {st.session_state.email}")

    with st.sidebar:
        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = api_get("/history", st.session_state.token) or []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if pergunta := st.chat_input("Digite sua pergunta:"):

        st.session_state.messages.append({"role": "user", "content": pergunta})
        st.chat_message("user").write(pergunta)

        resp = api_post("/chat", {"input": pergunta}, st.session_state.token)
        resposta_texto = resp["response"] if resp else "Erro ao obter resposta da API."

        st.session_state.messages.append({"role": "assistant", "content": resposta_texto})
        st.chat_message("assistant").write(resposta_texto)

if __name__ == "__main__":
    main()