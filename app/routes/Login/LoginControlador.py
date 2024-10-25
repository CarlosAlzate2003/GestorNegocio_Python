from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from app.schemas.usuario.usuarioDTO import loginDTO
from app.security.jwt_manager import create_token

router = APIRouter()


@router.post("/")
def login(usuario: loginDTO):
    if usuario.username == "admin" and usuario.password == "admin":
        token: str = create_token(usuario.dict())
        return JSONResponse(status_code=200, content=token)
    return JSONResponse(status_code=401, content={"message": "Usuario incorrecto"})
