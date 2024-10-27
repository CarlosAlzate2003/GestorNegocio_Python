from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.Config import get_db, SessionLocal, engine
from app.schemas.bodega.bodegaDTO import productosDTORequest, productosDTOResponse
from app.security.jwt_manager import JWTBearer
from app.models.Tables import productos

router = APIRouter()


@router.get(
    "/productos",
    response_model=list[productosDTOResponse],
    dependencies=[Depends(JWTBearer())],
)
async def Traer_Bodega():
    return productos


@router.get(
    "/productos/{id}", response_model=productosDTOResponse, summary="Trae sus productos"
)
async def Traer_Producto(id: int):
    for producto in productos:
        if producto["id"] == id:
            return producto
    return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})


@router.get("/productos/")
async def Traer_Producto_PorCategoria(categoria: str):
    return [producto for producto in productos if producto["categoria"] == categoria]


@router.post(
    "/productos", response_model=productosDTOResponse, summary="Agrega productos"
)
async def Agregar_Producto(data: productosDTORequest, db: Session = Depends(get_db)):
    try:
        producto = productos(
            nombre=data.nombre,
            categoria=data.categoria,
            precio=data.precio,
            cantidad=data.cantidad,
        )
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return JSONResponse(status_code=201, content={"message": "Producto agregado"})
    except Exception as e:
        db.rollback()
        raise e


@router.put("/productos/{id}")
async def Actualizar_Producto(id: int, producto: productosDTORequest):
    for producto in productos:
        if producto["id"] == id:
            producto["nombre"] = producto.nombre
            producto["categoria"] = producto.categoria
            producto["precio"] = producto.precio
            producto["cantidad"] = producto.cantidad
            return JSONResponse(
                status_code=201, content={"message": "Producto actualizado"}
            )
    return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})


@router.delete("/productos/{id}")
async def Eliminar_Producto(id: int):
    for producto in productos:
        if producto["id"] == id:
            productos.remove(producto)
            return JSONResponse(
                status_code=200, content={"message": "Producto eliminado"}
            )
    return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})
