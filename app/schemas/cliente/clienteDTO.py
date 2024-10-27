from pydantic import BaseModel, Field
from typing import Optional


class clienteDTORequest(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1, max_length=50)
    direccion: str = Field(min_length=1, max_length=50)
    telefono: str = Field(min_length=1, max_length=50)
    correo: str = Field(min_length=1, max_length=50)

    class Config:
        orm_mode = True


class clienteDTOResponse(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1, max_length=50)
    direccion: str = Field(min_length=1, max_length=50)
    telefono: str = Field(min_length=1, max_length=50)
    correo: str = Field(min_length=1, max_length=50)

    class Config:
        orm_mode = True
