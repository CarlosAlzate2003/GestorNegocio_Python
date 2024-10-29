from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.schemas.usuario.loginDTO import loginDTORequest
from app.models.Tables import usuarios
from app.security.jwt_manager import create_token
from app.database.Config import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter()


@router.post("/", summary="Ingresar tu usuario")
def login(dataUser: loginDTORequest, db: Session = Depends(get_db)):
    try:
        usuario = (
            db.query(usuarios)
            .filter(
                usuarios.correo == dataUser.correo,
                usuarios.contrasena == dataUser.contrasena,
            )
            .first()
        )
        if usuario:
            token: str = create_token({"id": usuario.id, "correo": usuario.correo})
            return JSONResponse(status_code=200, content=token)
        else:
            return JSONResponse(
                status_code=401, content={"message": "Usuario incorrecto"}
            )
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
    # token: str = create_token(usuario.dict())
    # return JSONResponse(status_code=200, content=token)
    # return JSONResponse(status_code=401, content={"message": "Usuario incorrecto"})
