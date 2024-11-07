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
            cedula=dataUser.cedula,
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


@router.put(
    "/update/{id}",
    response_model=usuarioDTOresponse,
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Actualiza sus usuarios",
)
async def Actualizar_Usuario(
    id: int,
    usuario: usuarioDTOrequest,
    db: Session = Depends(get_db),
):
    usuario_Actualizar = db.query(usuarios).filter(usuarios.id == id).first()
    if usuario_Actualizar:
        usuario_Actualizar.nombre = usuario.nombre
        usuario_Actualizar.cedula = usuario.cedula
        usuario_Actualizar.correo = usuario.correo
        usuario_Actualizar.contrasena = usuario.contrasena
        usuario_Actualizar.fk_rol = usuario.rol
        usuario_Actualizar.estado = usuario.estado
        db.commit()
        db.refresh(usuario_Actualizar)
        return usuario_Actualizar
    else:
        return JSONResponse(
            status_code=404, content={"message": "Usuario no encontrado"}
        )


@router.patch(
    "/disable/{id}",
    response_model=usuarioDTOresponse,
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Desactiva sus usuarios",
)
async def Desactivar_Usuario(
    id: int,
    db: Session = Depends(get_db),
):
    usuario_Actualizar = db.query(usuarios).filter(usuarios.id == id).first()
    if usuario_Actualizar:
        usuario_Actualizar.estado = False
        db.commit()
        db.refresh(usuario_Actualizar)
        return usuario_Actualizar
    else:
        return JSONResponse(
            status_code=404, content={"message": "Usuario no encontrado"}
        )
