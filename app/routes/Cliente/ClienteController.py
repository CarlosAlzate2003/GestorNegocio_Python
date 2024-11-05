from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.Config import get_db
from app.models.Tables import cliente
from app.schemas.cliente.clienteDTO import clienteDTORequest, clienteDTOResponse
from app.security.jwt_manager import JWTBearer

router = APIRouter()


@router.get(
    "/get_list",
    dependencies=[Depends(JWTBearer())],
    summary="Obtiene todos los clientes",
    response_model=list[clienteDTOResponse],
)
async def Obtener_Clientes(db: Session = Depends(get_db)):
    clientes = db.query(cliente).all()
    return clientes


@router.get(
    "/{id}",
    dependencies=[Depends(JWTBearer())],
    summary="Obtiene un cliente",
    response_model=clienteDTOResponse,
)
async def Obtener_Cliente(id: int, db: Session = Depends(get_db)):
    cliente_get = db.query(cliente).filter(cliente.id == id).first()
    if cliente_get:
        return cliente_get
    else:
        return JSONResponse(
            status_code=404, content={"message": "Este cliente no existe"}
        )


@router.post(
    "/create",
    response_model=clienteDTOResponse,
    dependencies=[Depends(JWTBearer())],
    summary="Agrega un cliente",
)
async def Agregar_Cliente(data: clienteDTORequest, db: Session = Depends(get_db)):
    try:
        cliente_add = cliente(
            nombre=data.nombre,
            direccion=data.direccion,
            telefono=data.telefono,
            correo=data.correo,
        )
        db.add(cliente_add)
        db.commit()
        db.refresh(cliente_add)
        return JSONResponse(status_code=201, content={"message": "Cliente agregado"})
    except Exception as e:
        db.rollback()
        raise e


@router.put(
    "/update/{id}",
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Actualiza un cliente",
)
async def Actualizar_Cliente(
    id: int,
    data: clienteDTORequest,
    db: Session = Depends(get_db),
):
    cliente_update = db.query(cliente).filter(cliente.id == id).first()
    if cliente_update:
        cliente_update.nombre = data.nombre
        cliente_update.direccion = data.direccion
        cliente_update.telefono = data.telefono
        cliente_update.correo = data.correo
        db.commit()
        db.refresh(cliente_update)
        return JSONResponse(status_code=200, content={"message": "Cliente actualizado"})
    else:
        return JSONResponse(
            status_code=404, content={"message": "Este cliente no existe"}
        )
