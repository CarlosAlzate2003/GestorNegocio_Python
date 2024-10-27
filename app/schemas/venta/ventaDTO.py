from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.productos.productosDTO import productosDTOResponse
from app.schemas.factura.facturaDTO import facturaDTOResponse


# class venta(Base):
#     __tablename__ = "venta"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     fecha_venta = Column(DateTime, nullable=False)
#     total_venta = Column(Float, nullable=False)
#     cantidad_producto = Column(Integer, nullable=False)
#     fk_producto = Column(
#         Integer,
#         ForeignKey("productos.id", ondelete="CASCADE"),
#         nullable=False,
#         index=True,
#     )
#     fk_factura = Column(
#         Integer,
#         ForeignKey("factura.id", ondelete="CASCADE"),
#         nullable=False,
#         index=True,
#     )
#     producto = relationship("productos", backref="venta", passive_deletes=True)
#     factura = relationship("factura", backref="venta", passive_deletes=True)


class ventaDTORequest(BaseModel):
    id: Optional[int] = None
    fecha_venta: datetime
    total_venta: float
    cantidad_producto: int
    fk_producto: int
    fk_factura: int

    class Config:
        orm_mode = True


class ventaDTOresponse(BaseModel):
    fecha_venta: datetime
    total_venta: float
    cantidad_producto: int
    producto: productosDTOResponse
    factura: facturaDTOResponse

    class Config:
        orm_mode = True
