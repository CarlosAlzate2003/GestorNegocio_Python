from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.Config import get_db
from app.schemas.proveedor.proveedorDTO import (
    proveedoresDTORequest,
    proveedoresDTOResponse,
)
from app.models.Tables import proveedores
from app.security.jwt_manager import JWTBearer

router = APIRouter()


@router.get(
    "/get_list",
    response_model=list[proveedoresDTOResponse],
    dependencies=[Depends(JWTBearer())],
)
async def Traer_Proveedores(db: Session = Depends(get_db)):
    proveedores_list = db.query(proveedores).all()
    return proveedores_list


@router.get(
    "/get/{id}",
    response_model=proveedoresDTOResponse,
    dependencies=[Depends(JWTBearer())],
    summary="Trae sus proveedores",
)
async def Traer_Proveedor(id: int, db: Session = Depends(get_db)):
    proveedor = db.query(proveedores).filter(proveedores.id == id).first()
    if proveedor:
        return proveedor
    else:
        return JSONResponse(
            status_code=404, content={"message": "Proveedor no encontrado"}
        )


@router.post(
    "/create",
    response_model=proveedoresDTOResponse,
    dependencies=[Depends(JWTBearer())],
    summary="Agrega proveedores",
)
async def Agregar_Proveedor(data: proveedoresDTORequest, db: Session = Depends(get_db)):
    try:
        proveedor = proveedores(
            nombre=data.nombre,
            direccion=data.direccion,
            telefono=data.telefono,
            correo=data.correo,
            estado=data.estado,
        )
        db.add(proveedor)
        db.commit()
        db.refresh(proveedor)
        return JSONResponse(status_code=201, content={"message": "Proveedor agregado"})
    except Exception as e:
        db.rollback()
        raise e


@router.put(
    "/update/{id}",
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Actualiza sus proveedores",
)
async def Actualizar_Proveedor(
    id: int,
    proveedor: proveedoresDTORequest,
    db: Session = Depends(get_db),
):
    proveedor_Actualizar = db.query(proveedores).filter(proveedores.id == id).first()
    if proveedor_Actualizar:
        proveedor_Actualizar.nombre = proveedor.nombre
        proveedor_Actualizar.direccion = proveedor.direccion
        proveedor_Actualizar.telefono = proveedor.telefono
        proveedor_Actualizar.correo = proveedor.correo
        db.commit()
        db.refresh(proveedor_Actualizar)
        return proveedor_Actualizar
    else:
        return JSONResponse(
            status_code=404, content={"message": "Proveedor no encontrado"}
        )


@router.delete(
    "/delete/{id}",
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Elimina sus proveedores",
)
async def Eliminar_Proveedor(
    id: int,
    db: Session = Depends(get_db),
):
    proveedor = db.query(proveedores).filter(proveedores.id == id).first()
    if proveedor:
        db.delete(proveedor)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Proveedor eliminado"})
    else:
        return JSONResponse(
            status_code=404, content={"message": "Proveedor no encontrado"}
        )


@router.patch(
    "/disable/{id}",
    response_model=proveedoresDTOResponse,
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Desactiva sus proveedores",
)
async def Desactivar_Proveedor(
    id: int,
    db: Session = Depends(get_db),
):
    proveedor = db.query(proveedores).filter(proveedores.id == id).first()
    if proveedor:
        proveedor.estado = False
        db.commit()
        db.refresh(proveedor)
        return proveedor
    else:
        return JSONResponse(
            status_code=404, content={"message": "Proveedor no encontrado"}
        )
