from pydantic import BaseModel, Field


class loginDTORequest(BaseModel):
    correo: str = Field(..., min_length=3, max_length=50)
    contrasena: str = Field(..., min_length=3, max_length=50)

    class Config:
        orm_mode = True
