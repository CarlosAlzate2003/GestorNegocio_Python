from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.cliente.clienteDTO import clienteDTOResponse
from app.schemas.usuario.usuarioDTO import usuarioDTOresponse


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
    fecha_factura: datetime = Field(...)
    total_factura: float = Field(...)
    cantidad_total_productos: int = Field(...)
    usuarios: usuarioDTOresponse = Field(...)
    cliente: clienteDTOResponse = Field(...)

    class Config:
        orm_mode = True
