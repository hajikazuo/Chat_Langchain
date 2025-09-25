from fastapi import FastAPI, HTTPException, Depends, Body
from passlib.context import CryptContext
from datetime import datetime
from chat import chat_assistant
from db import users_col, messages_col
from auth import create_jwt, get_current_user
from models import RegisterRequest, LoginRequest, ChatRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI(title="Assistente Educação Financeira API")

@app.post("/register")
def register(req: RegisterRequest):
    if users_col.find_one({"email": req.email}):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    hashed = pwd_context.hash(req.password)
    user = {"email": req.email, "password_hash": hashed, "created_at": datetime.utcnow()}
    result = users_col.insert_one(user)
    return {"user_id": str(result.inserted_id)}

@app.post("/login")
def login(req: LoginRequest):
    user = users_col.find_one({"email": req.email})
    if not user or not pwd_context.verify(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = create_jwt(str(user["_id"]))
    return {"access_token": token}

@app.post("/chat")
def chat(req: ChatRequest, user_id: str = Depends(get_current_user)):
    messages_col.insert_one({
        "session_id": user_id,
        "role": "user",
        "content": req.input,
        "timestamp": datetime.utcnow()
    })

    resposta = chat_assistant(user_id, req.input)

    messages_col.insert_one({
        "session_id": user_id,
        "role": "assistant",
        "content": resposta,
        "timestamp": datetime.utcnow()
    })

    return {"response": resposta}

@app.get("/history")
def history(user_id: str = Depends(get_current_user)):
    msgs = messages_col.find({"session_id": user_id}).sort("timestamp", 1)
    return [{"role": m["role"], "content": m["content"], "timestamp": m["timestamp"]} for m in msgs]
