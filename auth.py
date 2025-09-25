from fastapi import Depends, HTTPException, Header
from fastapi.security import APIKeyHeader
import jwt
from dotenv import load_dotenv
import os
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "minha_chave_secreta")
JWT_ALGORITHM = "HS256"

oauth2_scheme = APIKeyHeader(name="Authorization", scheme_name="Bearer")

def create_jwt(user_id: str):
    import datetime
    payload = {
        "sub": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except:
        return None

def get_current_user(authorization: str = Depends(oauth2_scheme)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token inválido")
    token = authorization.split(" ")[1]
    user_id = decode_jwt(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token expirado ou inválido")
    return user_id
