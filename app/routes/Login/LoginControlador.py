from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.schemas.usuario.loginDTO import loginRequest
from app.security.jwt_manager import create_token
from app.database.Config import get_db
from app.models.Tables import usuarios, rol

router = APIRouter()


@router.post("/", summary="Ingresa el login")
def login(dataUser: loginRequest, db: Session = Depends(get_db)):
    try:
        user = (
            db.query(usuarios)
            .filter(
                usuarios.correo == dataUser.correo,
                usuarios.contrasena == dataUser.contrasena,
            )
            .first()
        )
        if user:
            if user.estado == False:
                return JSONResponse(
                    status_code=401, content={"message": "Usuario inactivo"}
                )

            rolUser = db.query(rol).filter(rol.id == user.fk_rol).first()
            if rolUser == None:
                return JSONResponse(
                    status_code=401, content={"message": "Usuario incorrecto"}
                )

            token_data = dataUser.dict()
            token_data.update({"rol": rolUser.id})
            token_data.update({"id": user.id})

            token: str = create_token(token_data)
            return JSONResponse(
                status_code=200, content={"access_token": token, "token_type": "bearer"}
            )

    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={"message": "Fallo al loguear"})
