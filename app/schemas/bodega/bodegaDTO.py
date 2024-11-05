from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.proveedor.proveedorDTO import proveedoresDTOResponseProductos
from app.schemas.categoria.categoriaDTO import categoria_productoDTOResponseProductos


class productosDTORequest(BaseModel):
    id: Optional[int] = None
    nombre_producto: str = Field(min_length=1)
    descripcion: str = Field(min_length=1)
    cantidad: int = Field(gt=0)
    precio: float = Field(gt=0)
    fecha_ingreso: datetime = Field(default_factory=datetime.now)
    fk_proveedor: int = Field(gt=0)
    fk_categoria: int = Field(gt=0)

    class Config:
        orm_mode = True


class productosDTOResponse(BaseModel):
    nombre_producto: str = Field(min_length=1)
    descripcion: str = Field(min_length=1)
    cantidad: int = Field(gt=0)
    precio: float = Field(gt=0)
    fecha_ingreso: datetime = Field(default_factory=datetime.now)
    proveedor: proveedoresDTOResponseProductos
    categoria: categoria_productoDTOResponseProductos

    class Config:
        orm_mode = True
