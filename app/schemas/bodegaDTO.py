from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class productosDTORequest(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1)
    categoria: str = Field(min_length=1)
    precio: float = Field(gt=0)
    cantidad: int = Field(gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Producto",
                "categoria": "Categoria",
                "precio": 1000,
                "cantidad": 10,
            }
        }


class productosDTOResponse(BaseModel):
    nombre: str = Field(min_length=1)
    categoria: str = Field(min_length=1)
    precio: float = Field(gt=0)
    cantidad: int = Field(gt=0)
