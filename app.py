import streamlit as st
from chat import chat_assistant

st.set_page_config(page_title="Assistente de Educação Financeira", page_icon="💰")
st.title("💬 Assistente de Educação Financeira")
st.caption("🚀 Seu guia para organizar, poupar e investir melhor")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Olá! Eu sou seu assistente financeiro. "
                                         "Antes de começarmos, me conte: "
                                         "qual é sua principal meta financeira (ex: quitar dívidas, comprar casa, investir)?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if pergunta := st.chat_input("Pergunte alguma coisa:"):

    st.session_state.messages.append({"role": "user", "content": pergunta})
    st.chat_message("user").write(pergunta)

    resposta = chat_assistant("user123", pergunta)

    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.chat_message("assistant").write(resposta)

