import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory

template = """[INST]Você é um assistente de educação financeira.  
Ajude o usuário a aprender sobre finanças pessoais com dicas práticas, exemplos e explicações fáceis.  

Sempre comece perguntando:
1. Qual a principal meta financeira do usuário? (ex: comprar casa, quitar dívidas, investir)
2. Qual a renda mensal aproximada?
3. Quais gastos fixos mais pesam no orçamento?

Histórico da conversa:
{history}

Pergunta do usuário: {input}"""

prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

llm = ChatGroq(
    model="llama-3.1-8b-instant",  
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
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

def chat_assistant(session_id: str, texto: str) -> str:
    response = chain_with_history.invoke(
        {"input": texto},
        config={"configurable": {"session_id": session_id}}
    )
    return response.content

