from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import pandas
from app.database.Config import get_db
from app.models.Tables import productos, proveedores, categoria_producto
from app.security.jwt_manager import JWTBearer

#  get_current_role
router = APIRouter()


@router.post(
    "/cargar_productos",
    dependencies=[Depends(JWTBearer(required_roles=[1]))],
    summary="Carga masiva de productos con Excel",
)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if (
        file.content_type
        != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    ):
        raise HTTPException(status_code=400, detail="El archivo no es un Excel")

    try:
        content = await file.read()
        df = pandas.read_excel(content)

        expected_columns = [
            "nombre_producto",
            "descripcion",
            "cantidad",
            "precio",
            "proveedor",
            "categoria",
        ]

        if not all(column in df.columns for column in expected_columns):
            raise HTTPException(
                status_code=400,
                detail="El archivo Excel no contiene las columnas esperadas",
            )

        for _, row in df.iterrows():
            categoria_nombre = row["categoria"]
            categoria = (
                db.query(categoria_producto)
                .filter(categoria_producto.nombre == categoria_nombre)
                .first()
            )
            if not categoria:
                categoria = categoria_producto(
                    nombre=categoria_nombre, descripcion="Default"
                )
                db.add(categoria)
                db.commit()
                db.refresh(categoria)

            proveedor_nombre = row["proveedor"]
            proveedor = (
                db.query(proveedores)
                .filter(proveedores.nombre == proveedor_nombre)
                .first()
            )
            if not proveedor:
                proveedor = proveedores(
                    nombre=proveedor_nombre,
                    direccion="Default",
                    telefono="Default",
                    correo="Default",
                    estado=True,
                )
                db.add(proveedor)
                db.commit()
                db.refresh(proveedor)

            nuevo_producto = productos(
                nombre_producto=row["nombre_producto"],
                descripcion=row["descripcion"],
                cantidad=row["cantidad"],
                precio=row["precio"],
                fecha_ingreso=datetime.now(),
                fk_proveedor=categoria.id,
                fk_categoria=proveedor.id,
            )
            db.add(nuevo_producto)
            db.commit()
        return JSONResponse(status_code=201, content={"message": "Productos agregados"})
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error de integridad de datos")
