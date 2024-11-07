from pydantic import BaseModel
from datetime import datetime
from app.schemas.bodega.bodegaDTO import productosDTOResponseVenta


class ventaDTOresponse(BaseModel):
    fecha_venta: datetime
    total_venta: float
    cantidad_producto: int
    producto: productosDTOResponseVenta

    class Config:
        orm_mode = True
