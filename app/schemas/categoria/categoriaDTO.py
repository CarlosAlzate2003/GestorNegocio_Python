from pydantic import BaseModel, Field
from typing import Optional


class categoria_productoDTORequest(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1)
    descripcion: str = Field(min_length=1)

    class Config:
        orm_mode = True


class categoria_productoDTOResponse(BaseModel):
    nombre: str = Field(min_length=1)
    descripcion: str = Field(min_length=1)

    class Config:
        orm_mode = True
