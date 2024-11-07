from pydantic import BaseModel, Field
from typing import Optional
from typing import List


class clienteDTORequest(BaseModel):
    id: Optional[int] = None
    cedula: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=1, max_length=50)
    direccion: str = Field(min_length=1, max_length=50)
    telefono: str = Field(min_length=1, max_length=50)
    correo: str = Field(min_length=1, max_length=50)

    class Config:
        orm_mode = True


class clienteDTOResponse(BaseModel):
    id: Optional[int] = None
    cedula: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=1, max_length=50)
    direccion: str = Field(min_length=1, max_length=50)
    telefono: str = Field(min_length=1, max_length=50)
    correo: str = Field(min_length=1, max_length=50)

    class Config:
        orm_mode = True


class clienteDTOResponseFactura(BaseModel):
    cedula: str = Field(min_length=1, max_length=50)
    nombre: str = Field(min_length=1, max_length=50)

    class Config:
        orm_mode = True
