from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.schemas.rol.rolDTO import rolDTOresponse


class usuarioDTOrequest(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=3, max_length=50)
    correo: str = Field(..., min_length=3, max_length=50)
    contrasena: str = Field(..., min_length=3, max_length=50)
    rol: int
    estado: bool = Field(...)
    fecha_creacion: datetime = Field(default=datetime.now())

    class Config:
        orm_mode = True


class usuarioDTOresponse(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    correo: str = Field(..., min_length=3, max_length=50)
    contrasena: str = Field(..., min_length=3, max_length=50)
    rol: rolDTOresponse
    estado: bool = Field(...)
    fecha_creacion: datetime = Field(default=datetime.now())

    class Config:
        orm_mode = True
