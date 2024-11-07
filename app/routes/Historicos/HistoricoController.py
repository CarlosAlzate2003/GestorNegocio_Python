from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database.Config import get_db
from app.models.Tables import factura, venta, cliente, productos
from fastapi.responses import JSONResponse
from app.schemas.factura.facturaDTO import facturaDTOResponse
from app.schemas.venta.ventaDTO import ventaDTOresponse
from app.security.jwt_manager import JWTBearer
from datetime import datetime
from sqlalchemy import func
import pandas as pd
from sqlalchemy.orm import aliased

router = APIRouter()


# traer todas las facturaciones
@router.get(
    "/getall",
    response_model=list[facturaDTOResponse],
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Trae todas las facturas",
)
async def get_all_facturas(db: Session = Depends(get_db)):
    facturas = db.query(factura).all()
    return facturas


# eliminar factura
@router.delete(
    "/delete/{id}",
    response_model=facturaDTOResponse,
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Elimina una factura",
)
async def delete_factura(id: int, db: Session = Depends(get_db)):
    factura_db = db.query(factura).filter(factura.id == id).first()
    if factura_db:
        db.delete(factura_db)
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Factura eliminada"})
    else:
        return JSONResponse(
            status_code=404, content={"message": "Factura no encontrada"}
        )


# traer facturas entre fechas
@router.get(
    "/getbetween",
    response_model=list[facturaDTOResponse],
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Trae facturas entre fechas",
)
async def get_facturas_between_dates(
    fecha_inicio: str, fecha_fin: str, db: Session = Depends(get_db)
):
    start_date = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    end_date = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    facturas = (
        db.query(factura)
        .filter(func.date(factura.fecha_factura).between(start_date, end_date))
        .all()
    )
    if facturas:
        return facturas
    else:
        return JSONResponse(
            status_code=404, content={"message": "Facturas no encontradas"}
        )


# traer facturas de un usuario
@router.get(
    "/getbyuser/{id}",
    response_model=list[facturaDTOResponse],
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Trae facturas de un usuario",
)
async def get_factura_by_user(id: int, db: Session = Depends(get_db)):
    facturas = db.query(factura).filter(factura.fk_usuarios == id).all()
    if facturas:
        return facturas
    else:
        return JSONResponse(
            status_code=404, content={"message": "Facturas no encontradas"}
        )


# traer facturas de un cliente
@router.get(
    "/getbyclient/{id}",
    response_model=list[facturaDTOResponse],
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Trae facturas de un cliente",
)
async def get_factura_by_client(id: int, db: Session = Depends(get_db)):
    facturas = (
        db.query(factura)
        .join(cliente, factura.fk_cliente == cliente.id)
        .filter(cliente.id == id)
        .all()
    )
    if facturas:
        return facturas
    else:
        return JSONResponse(
            status_code=404, content={"message": "Facturas no encontradas"}
        )


# traer ventas de una factura
@router.get(
    "/getventasbyfactura/{id}",
    response_model=list[ventaDTOresponse],
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Trae ventas de una factura",
)
async def get_ventas_by_factura(id: int, db: Session = Depends(get_db)):
    ventas = db.query(venta).filter(venta.fk_factura == id).all()
    if ventas:
        return ventas
    else:
        return JSONResponse(
            status_code=404, content={"message": "Ventas no encontradas"}
        )


# traer total vendido en un dia
@router.get(
    "/gettotalbyday/{fecha}",
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Trae total vendido en un dia",
)
async def get_total_by_day(fecha: str, db: Session = Depends(get_db)):
    fecha_total = datetime.strptime(fecha, "%Y-%m-%d").date()
    ventas = db.query(venta).filter(func.date(venta.fecha_venta) == fecha_total).all()
    total = 0
    for venta_db in ventas:
        total += venta_db.total_venta
    return JSONResponse(
        status_code=200, content={f"total vendido el dia {fecha_total}": total}
    )


# traer total vendido en un mes
@router.get(
    "/gettotalbymonth/{year}/{month}",
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Trae total vendido en un mes",
)
async def get_total_by_month(year: int, month: int, db: Session = Depends(get_db)):
    # Verifica que el mes esté en el rango correcto
    if month < 1 or month > 12:
        return JSONResponse(status_code=400, content={"message": "Mes inválido"})

    # Filtra las ventas para el año y mes especificado
    ventas = (
        db.query(venta)
        .filter(func.extract("year", venta.fecha_venta) == year)
        .filter(func.extract("month", venta.fecha_venta) == month)
        .all()
    )

    # Suma el total de ventas
    total = sum(venta_db.total_venta for venta_db in ventas)

    return JSONResponse(
        status_code=200, content={f"total vendido en {year}-{month:02d}": total}
    )


@router.get(
    "/generarexcel/{fecha_inicio}/{fecha_fin}",
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Genera excel entre fechas",
)
async def generar_excel(
    fecha_inicio: str, fecha_fin: str, db: Session = Depends(get_db)
):
    # Convertir las fechas de entrada
    start_date = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    end_date = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    # Crear alias para las tablas para facilitar la unión
    venta_alias = aliased(venta)
    productos_alias = aliased(productos)

    # Realizar la consulta con las uniones
    facturas_ventas_productos = (
        db.query(
            factura.id.label("ID_Factura"),
            factura.fecha_factura.label("Fecha_Factura"),
            factura.total_factura.label("Total_Factura"),
            factura.fk_usuarios.label("ID_Usuario"),
            factura.fk_cliente.label("ID_Cliente"),
            venta_alias.id.label("ID_Venta"),
            venta_alias.total_venta.label("Total_Venta"),
            venta_alias.cantidad_producto.label("Cantidad"),
            factura.cantidad_total_productos.label("Cantidad_Total_Productos"),
            productos_alias.nombre_producto.label("Producto"),
        )
        .join(venta_alias, venta_alias.fk_factura == factura.id)
        .join(productos_alias, productos_alias.id == venta_alias.fk_producto)
        .filter(factura.fecha_factura.between(start_date, end_date))
        .all()
    )

    # Si hay datos, procesarlos
    if facturas_ventas_productos:
        # Convertir cada fila de la consulta en un diccionario
        data = []
        for factura_venta_producto in facturas_ventas_productos:
            data.append(
                {
                    "ID Factura": factura_venta_producto.ID_Factura,
                    "Fecha Factura": factura_venta_producto.Fecha_Factura,
                    "Total Factura": factura_venta_producto.Total_Factura,
                    "ID Usuario": factura_venta_producto.ID_Usuario,
                    "ID Cliente": factura_venta_producto.ID_Cliente,
                    "ID Venta": factura_venta_producto.ID_Venta,
                    "Producto": factura_venta_producto.Producto,
                    "Cantidad Producto": factura_venta_producto.Cantidad,
                    "Precio Producto": factura_venta_producto.Total_Venta,
                    "Cantidad Total Productos": factura_venta_producto.Cantidad_Total_Productos,
                }
            )

        # Crear el DataFrame
        df = pd.DataFrame(data)

        # Generar el archivo Excel
        excel_file = "facturas_ventas_productos.xlsx"
        df.to_excel(excel_file, index=False)

        # Enviar el archivo Excel como respuesta
        return FileResponse(
            path=excel_file,
            filename=excel_file,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        return JSONResponse(
            status_code=404,
            content={
                "message": "No se encontraron registros para las fechas indicadas"
            },
        )
