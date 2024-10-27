from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class rol(Base):
    __tablename__ = "rol"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)


class usuarios(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    correo = Column(String(50), nullable=False)
    contrasena = Column(String(50), nullable=False)
    fk_rol = Column(Integer, ForeignKey("rol.id"), nullable=False, index=True)
    rol = relationship("rol", backref="usuario")
    estado = Column(Boolean, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)


class proveedores(Base):
    __tablename__ = "proveedores"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    direccion = Column(String(50), nullable=False)
    telefono = Column(String(50), nullable=False)
    correo = Column(String(50), nullable=False)
    estado = Column(Boolean, nullable=False)


class categoria_producto(Base):
    __tablename__ = "categoria_producto"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    descripcion = Column(String(50), nullable=True)


class productos(Base):
    __tablename__ = "productos"
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
    proveedor = relationship("proveedores", backref="producto")
    categoria = relationship("categoria_producto", backref="producto")


class cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    direccion = Column(String(50), nullable=False)
    telefono = Column(String(50), nullable=False)
    correo = Column(String(50), nullable=False)


class factura(Base):
    __tablename__ = "factura"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_factura = Column(DateTime, nullable=False)
    total_factura = Column(Float, nullable=False)
    cantidad_total_productos = Column(Integer, nullable=False)
    fk_usuarios = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False,
        index=True,
    )
    fk_cliente = Column(
        Integer,
        ForeignKey("cliente.id"),
        nullable=False,
        index=True,
    )
    cliente = relationship("cliente", backref="venta")
    usuarios = relationship("usuarios", backref="factura")


class venta(Base):
    __tablename__ = "venta"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha_venta = Column(DateTime, nullable=False)
    total_venta = Column(Float, nullable=False)
    cantidad_producto = Column(Integer, nullable=False)
    fk_producto = Column(
        Integer,
        ForeignKey("productos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    fk_factura = Column(
        Integer,
        ForeignKey("factura.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    producto = relationship("productos", backref="venta", passive_deletes=True)
    factura = relationship("factura", backref="venta", passive_deletes=True)
