from pydantic import BaseModel, Field
from datetime import datetime
from app.schemas.rol.rolDTO import rolDTOresponse


class loginRequest(BaseModel):
    correo: str = Field(..., min_length=3, max_length=50)
    contrasena: str = Field(..., min_length=3, max_length=50)

    class Config:
        orm_mode = True


class loginResponse(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    correo: str = Field(..., min_length=3, max_length=50)
    contrasena: str = Field(..., min_length=3, max_length=50)
    rol: rolDTOresponse
    estado: bool = Field(...)
    fecha_creacion: datetime = Field(default=datetime.now())

    class Config:
        orm_mode = True
