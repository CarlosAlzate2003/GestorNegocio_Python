from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.Config import get_db
from app.schemas.usuario.usuarioDTO import usuarioDTOrequest, usuarioDTOresponse
from app.security.jwt_manager import JWTBearer
from app.models.Tables import usuarios

router = APIRouter()


@router.post(
    "/crearusuario",
    response_model=usuarioDTOresponse,
    dependencies=[Depends(JWTBearer())],
)
async def crear_usuario(dataUser: usuarioDTOrequest, db: Session = Depends(get_db)):
    try:
        usuario = usuarios(
            nombre=dataUser.nombre,
            correo=dataUser.correo,
            contrasena=dataUser.contrasena,
            fk_rol=dataUser.rol,
            estado=dataUser.estado,
            fecha_creacion=dataUser.fecha_creacion,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return JSONResponse(status_code=201, content={"message": "Usuario creado"})
    except Exception as e:
        db.rollback()
        raise e
