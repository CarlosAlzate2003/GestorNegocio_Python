from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, JSONResponse
from app.schemas.usuario.loginDTO import loginRequest, loginResponse
from app.security.jwt_manager import create_token
from app.database.Config import SessionLocal, engine, get_db
from app.models.Tables import usuarios, rol

router = APIRouter()


# @router.post("/")
# def login(usuario: loginDTO):
#     # if usuario.username == "admin" and usuario.password == "admin":
#     #     token: str = create_token(usuario.dict())
#     #     return JSONResponse(status_code=200, content=token)
#     # return JSONResponse(status_code=401, content={"message": "Usuario incorrecto"})
#     try:
#         user
#     except Exception as e:
#         print(e)
#         return JSONResponse(status_code=401, content={"message": "Usuario incorrecto"})


@router.post("/", responnse_model=loginResponse, summary="Ingresa el login")
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
            rolUser = db.query(rol).filter(rol.id == user.fk_rol).first()
            if rolUser == None:
                return JSONResponse(
                    status_code=401, content={"message": "Usuario incorrecto"}
                )
            dataUser.rol = rolUser.id

            token: str = create_token(dataUser.dict())
            return JSONResponse(status_code=200, content=token)

    except Exception as e:
        print(e)
        return JSONResponse(status_code=401, content={"message": "Usuario incorrecto"})
    # token: str = create_token(dataUser.dict())
    # return JSONResponse(status_code=200, content=token)
