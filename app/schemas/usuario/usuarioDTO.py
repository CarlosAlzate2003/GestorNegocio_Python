from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional


class loginDTO(BaseModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=5)
