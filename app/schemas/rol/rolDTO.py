from pydantic import BaseModel, Field
from typing import Optional


class rolDTOrequest(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(..., min_length=3, max_length=50)

    class Config:
        orm_mode = True


class rolDTOresponse(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)

    class Config:
        orm_mode = True
