from pydantic import BaseModel, Field
from typing import Optional


class proveedoresDTORequest(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1)
    direccion: str = Field(min_length=1)
    telefono: str = Field(min_length=1)
    correo: str = Field(min_length=1)
    estado: bool = Field(default=True)

    class Config:
        orm_mode = True


class proveedoresDTOResponse(BaseModel):
    nombre: str = Field(min_length=1)
    direccion: str = Field(min_length=1)
    telefono: str = Field(min_length=1)
    correo: str = Field(min_length=1)
    estado: bool = Field(default=True)

    class Config:
        orm_mode = True
