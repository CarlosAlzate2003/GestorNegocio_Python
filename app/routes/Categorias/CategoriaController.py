from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.Config import get_db
from app.models.Tables import categoria_producto
from app.schemas.categoria.categoriaDTO import (
    categoria_productoDTORequest,
    categoria_productoDTOResponse,
)
from app.security.jwt_manager import JWTBearer

router = APIRouter()


@router.get(
    "/get_list",
    response_model=list[categoria_productoDTOResponse],
    dependencies=[Depends(JWTBearer())],
    summary="Obtiene todas las categorias",
)
async def Obtener_Categorias(db: Session = Depends(get_db)):
    categorias = db.query(categoria_producto).all()
    return categorias


@router.post(
    "/create",
    response_model=categoria_productoDTOResponse,
    dependencies=[Depends(JWTBearer())],
    summary="Agrega categorias",
)
async def Agregar_Categoria(
    data: categoria_productoDTORequest, db: Session = Depends(get_db)
):
    try:
        categoria = categoria_producto(
            nombre=data.nombre,
            descripcion=data.descripcion,
        )
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
        return JSONResponse(status_code=201, content={"message": "Categoria agregada"})
    except Exception as e:
        db.rollback()
        raise e


@router.delete(
    "/delete/{id}",
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Elimina categorias",
)
async def Eliminar_Categoria(
    id: int,
    db: Session = Depends(get_db),
):
    categoria = db.query(categoria_producto).filter(categoria_producto.id == id).first()
    if categoria:
        db.delete(categoria)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Categoria eliminada"})
    else:
        return JSONResponse(
            status_code=404, content={"message": "Esta categoria no existe"}
        )
