from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_token(data: dict):
    expiration = datetime.utcnow() + timedelta(minutes=50)
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
    def __init__(self, required_roles: list = None):
        super().__init__()
        self.required_roles = required_roles or []

    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        user_data = validate_token(auth.credentials)

        # Verificación del rol
        if self.required_roles:
            has_permission(user_data, self.required_roles)

        return user_data


def has_permission(data: dict, required_roles: list):
    if "rol" not in data:
        raise HTTPException(
            status_code=403, detail="No tiene permisos para realizar esta acción"
        )

    user_role = data["rol"]
    if user_role not in required_roles:
        raise HTTPException(
            status_code=403, detail="No tiene permisos para realizar esta acción"
        )
