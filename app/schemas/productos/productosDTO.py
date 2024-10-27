from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.proveedor.proveedorDTO import proveedoresDTOResponse
from app.schemas.categoria.categoriaDTO import categoria_productoDTOResponse


class productoDTORequest(BaseModel):
    id: Optional[int] = None
    nombre_producto: str = Field(..., min_length=3, max_length=50)
    descripcion: str = Field(..., min_length=3, max_length=50)
    cantidad: int = Field(..., gt=0)
    precio: float = Field(..., gt=0)
    fecha_ingreso: datetime = Field(default=datetime.now())
    fk_proveedor: int
    fk_categoria: int

    class Config:
        orm_mode = True


class productosDTOResponse(BaseModel):
    id: Optional[int] = None
    nombre_producto: str = Field(..., min_length=3, max_length=50)
    descripcion: str = Field(..., min_length=3, max_length=50)
    cantidad: int = Field(..., gt=0)
    precio: float = Field(..., gt=0)
    fecha_ingreso: datetime = Field(default=datetime.now())
    proveedor: proveedoresDTOResponse
    categoria: categoria_productoDTOResponse

    class Config:
        orm_mode = True
