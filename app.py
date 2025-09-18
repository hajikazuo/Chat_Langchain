import streamlit as st
from chat import chat_assistant

st.title("Assistente de Viagem")

if "session_id" not in st.session_state:
    st.session_state.session_id = "user123"
if "histórico" not in st.session_state:
    st.session_state.histórico = []
if "input" not in st.session_state:
    st.session_state.input = ""

def enviar_mensagem():
    if st.session_state.input:
        pergunta = st.session_state.input
        resposta = chat_assistant(st.session_state.session_id, pergunta)
        st.session_state.histórico.append(("Você", pergunta))
        st.session_state.histórico.append(("Assistente", resposta))
        st.session_state.input = ""

for speaker, message in st.session_state.histórico:
    if speaker == "Você":
        st.markdown(f"<div style='text-align: left; background-color:#DCF8C6; color:#000; padding:8px; border-radius:8px; margin:4px 0'>{message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; background-color:#FFF; color:#000; padding:8px; border-radius:8px; margin:4px 0'>{message}</div>", unsafe_allow_html=True)

st.text_input("Pergunte alguma coisa:", key="input", on_change=enviar_mensagem)