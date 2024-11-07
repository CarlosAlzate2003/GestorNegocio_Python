from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.Config import get_db
from app.schemas.bodega.bodegaDTO import productosDTORequestCompra
from app.models.Tables import productos, venta, factura, cliente
from app.security.jwt_manager import JWTBearer
from datetime import datetime
from fastapi import HTTPException


router = APIRouter()


@router.post(
    "/pay",
    dependencies=[Depends(JWTBearer())],
    summary="Pagar productos",
)
async def Pagar_Producto(
    cc_cliente: int,
    nombre_cliente: str,
    productos_compra: list[productosDTORequestCompra],
    db: Session = Depends(get_db),
    usuario_id: int = Depends(JWTBearer()),
):
    try:
        comprador = db.query(cliente).filter(cliente.cedula == cc_cliente).first()

        if not comprador:
            comprador = cliente(
                cedula=cc_cliente,
                nombre=nombre_cliente,
                direccion="Default",
                telefono="Default",
                correo="Default",
            )
            db.add(comprador)
            db.commit()
            db.refresh(comprador)

        nueva_factura = factura(
            fecha_factura=datetime.now(),
            total_factura=0,
            cantidad_total_productos=0,
            fk_usuarios=usuario_id,
            fk_cliente=comprador.id,
        )

        db.add(nueva_factura)
        db.commit()

        total_factura = 0
        cantidad_total_productos = 0

        for item in productos_compra:
            producto_db = db.query(productos).filter(productos.id == item.id).first()
            if producto_db and producto_db.cantidad >= item.cantidad:
                total_venta_producto = producto_db.precio * item.cantidad

                nueva_venta = venta(
                    fecha_venta=datetime.now(),
                    total_venta=total_venta_producto,
                    cantidad_producto=item.cantidad,
                    fk_factura=nueva_factura.id,
                    fk_producto=producto_db.id,
                )
                db.add(nueva_venta)
                producto_db.cantidad -= item.cantidad
                total_factura += total_venta_producto
                cantidad_total_productos += item.cantidad
            else:
                db.delete(nueva_factura)
                db.commit()
                db.rollback()
                return JSONResponse(
                    status_code=400,
                    content={"message": "No hay suficiente cantidad de productos"},
                )
        nueva_factura.total_factura = total_factura
        nueva_factura.cantidad_total_productos = cantidad_total_productos
        db.commit()

        return JSONResponse(
            status_code=201,
            content={
                "message": f"Compra realizada con exito. #factura:{nueva_factura.id}"
            },
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
