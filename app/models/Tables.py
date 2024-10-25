from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class usuarios(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    correo = Column(String(50), nullable=False)
    contrasena = Column(String(50), nullable=False)
    rol = Column(String(50), nullable=False)
    estado = Column(Boolean, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)


class proveedores(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    direccion = Column(String(50), nullable=False)
    telefono = Column(String(50), nullable=False)
    correo = Column(String(50), nullable=False)


class categoria_producto(Base):
    __tablename__ = "categoria_producto"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(50), nullable=True)


class bodega(Base):
    __tablename__ = "bodega"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_producto = Column(String(50), nullable=False)
    descripcion = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    fecha_ingreso = Column(DateTime, nullable=False)
    fk_proveedor = Column(
        Integer, ForeignKey("proveedores.id"), nullable=False, index=True
    )
    fk_categoria = Column(
        Integer, ForeignKey("categoria_producto.id"), nullable=False, index=True
    )


# falta cositas, revisa gepeto
