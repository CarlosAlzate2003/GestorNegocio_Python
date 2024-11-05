from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_token(data: dict):
    expiration = datetime.utcnow() + timedelta(minutes=50)  # Expirará en 30 minutos
    data.update({"exp": expiration})
    token: str = encode(payload=data, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def validate_token(token: str) -> dict:
    try:
        data: dict = decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return data
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        return data
