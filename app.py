import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

template = """[INST]Você é um assistente de viagem. Ajoute o usuário a planejar viagens com sugestões de destinos, roteiros e dicas práticas.
Sempre comece perguntando:
1. Para onde o usuário vai viajar?
2. Com quantas pessoas?
3. Por quantos dias?

Histórico da conversa:
{history}

Pergunta do usuário: {input}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])


llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-3.5-turbo"
)

chain = prompt | llm

store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

def iniciar_assistente_viagem():
    print("Bem-vindo ao Assistente de Viagem! Digite 'sair' para encerrar.\n")
    while True:
        user_input = input("Você: ")

        if user_input.lower() in ["sair", "exit"]:
            print("Até mais! Boa viagem!")
            break

        response = chain_with_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": 'user123'}}
        )


        print("Assistente:", response.content)

if __name__ == "__main__":
    iniciar_assistente_viagem()