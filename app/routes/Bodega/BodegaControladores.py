from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.Config import get_db
from app.schemas.bodega.bodegaDTO import productosDTORequest, productosDTOResponse
from app.security.jwt_manager import JWTBearer
from app.models.Tables import productos

router = APIRouter()


@router.get(
    "/productos",
    response_model=list[productosDTOResponse],
    dependencies=[Depends(JWTBearer())],
    summary="Trae sus productos",
)
async def Traer_Bodega(db: Session = Depends(get_db)):
    productos_list = db.query(productos).all()
    return productos_list


@router.get(
    "/productos/{id}",
    response_model=productosDTOResponse,
    dependencies=[Depends(JWTBearer())],
    summary="Trae sus productos",
)
async def Traer_Producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(productos).filter(productos.id == id).first()
    if producto:
        return producto
    else:
        return JSONResponse(
            status_code=404, content={"message": "Producto no encontrado"}
        )


@router.get(
    "/productos/categoria/{id}",
    dependencies=[Depends(JWTBearer())],
    summary="Trae sus productos por categoria",
)
async def Traer_Producto_PorCategoria(id: int, db: Session = Depends(get_db)):
    productos_list = db.query(productos).filter(productos.fk_categoria == id).all()
    if productos_list:
        return productos_list
    else:
        return JSONResponse(
            status_code=404, content={"message": "Esta categoria no existe"}
        )


@router.post(
    "/productos",
    response_model=productosDTOResponse,
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Agrega productos",
)
async def Agregar_Producto(data: productosDTORequest, db: Session = Depends(get_db)):
    try:
        producto = productos(
            nombre_producto=data.nombre_producto,
            descripcion=data.descripcion,
            precio=data.precio,
            cantidad=data.cantidad,
            fecha_ingreso=data.fecha_ingreso,
            fk_proveedor=data.fk_proveedor,
            fk_categoria=data.fk_categoria,
        )
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return JSONResponse(status_code=201, content={"message": "Producto agregado"})
    except Exception as e:
        db.rollback()
        raise e


@router.post(
    "/productos/addstock",
    response_model=productosDTOResponse,
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Agrega stock",
)
async def Agregar_Stock(id: int, cantidad: int, db: Session = Depends(get_db)):
    producto = db.query(productos).filter(productos.id == id).first()
    if producto:
        producto.cantidad += cantidad
        db.commit()
        db.refresh(producto)
        return producto
    else:
        return JSONResponse(
            status_code=404, content={"message": "Producto no encontrado"}
        )


@router.put(
    "/productos/{id}",
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Actualiza sus productos",
)
async def Actualizar_Producto(
    id: int, producto: productosDTORequest, db: Session = Depends(get_db)
):
    producto_actualizar = db.query(productos).filter(productos.id == id).first()
    if producto_actualizar:
        producto_actualizar.nombre_producto = producto.nombre_producto
        producto_actualizar.descripcion = producto.descripcion
        producto_actualizar.precio = producto.precio
        producto_actualizar.cantidad = producto.cantidad
        producto_actualizar.fk_proveedor = producto.fk_proveedor
        producto_actualizar.fk_categoria = producto.fk_categoria
        db.commit()
        db.refresh(producto_actualizar)
        return producto_actualizar
    else:
        return JSONResponse(
            status_code=404, content={"message": "Producto no encontrado"}
        )


@router.delete(
    "/productos/{id}",
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Elimina sus productos",
)
async def Eliminar_Producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(productos).filter(productos.id == id).first()
    if producto:
        db.delete(producto)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Producto eliminado"})
    else:
        return JSONResponse(
            status_code=404, content={"message": "Producto no encontrado"}
        )
