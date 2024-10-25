from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from datetime import datetime, timedelta


def create_token(data: dict):
    expiration = datetime.utcnow() + timedelta(minutes=50)  # Expirará en 30 minutos
    data.update({"exp": expiration})
    token: str = encode(payload=data, key="my_secret_key", algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    try:
        data: dict = decode(token, key="my_secret_key", algorithms=["HS256"])
        return data
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["username"] != "admin":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")
        return data
