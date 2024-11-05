from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database.Config import get_db
from app.schemas.bodega.bodegaDTO import productosDTORequest
from app.models.Tables import productos, cliente, proveedores, categoria_producto
