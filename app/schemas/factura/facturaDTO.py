from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.cliente.clienteDTO import clienteDTOResponseFactura
from app.schemas.usuario.usuarioDTO import usuarioDTOresponseFactura


class facturaDTORequest(BaseModel):
    id: Optional[int] = None
    fecha_factura: datetime = Field(...)
    total_factura: float = Field(...)
    cantidad_total_productos: int = Field(...)
    fk_usuarios: int = Field(...)
    fk_cliente: int = Field(...)

    class Config:
        orm_mode = True


class facturaDTOResponse(BaseModel):
    id: Optional[int] = None
    fecha_factura: datetime = Field(...)
    total_factura: float = Field(...)
    cantidad_total_productos: int = Field(...)
    usuarios: usuarioDTOresponseFactura = Field(...)
    cliente: clienteDTOResponseFactura = Field(...)

    class Config:
        orm_mode = True
