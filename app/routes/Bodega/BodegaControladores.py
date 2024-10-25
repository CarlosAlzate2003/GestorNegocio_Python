from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from app.schemas.bodegaDTO import productosDTORequest, productosDTOResponse

router = APIRouter()

productos = [
    {
        "id": 1,
        "nombre": "Manzana",
        "categoria": "frutas",
        "precio": 100,
        "cantidad": 10,
    },
    {
        "id": 2,
        "nombre": "Durazno",
        "categoria": "frutas",
        "precio": 200,
        "cantidad": 20,
    },
    {
        "id": 3,
        "nombre": "Zanahoria",
        "categoria": "frutas",
        "precio": 300,
        "cantidad": 30,
    },
]


@router.get("/", tags=["Default"])
async def Home():
    return HTMLResponse("<h1>Hello World</h1>")


@router.get("/productos", tags=["Bodega"], response_model=list[productosDTOResponse])
async def Traer_Bodega():
    return productos


@router.get("/productos/{id}", tags=["Bodega"], response_model=productosDTOResponse)
async def Traer_Producto(id: int):
    for producto in productos:
        if producto["id"] == id:
            return producto
    return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})


@router.get("/productos/", tags=["Bodega"])
async def Traer_Producto_PorCategoria(categoria: str):
    return [producto for producto in productos if producto["categoria"] == categoria]


@router.post("/productos", tags=["Bodega"])
async def Agregar_Producto(producto: productosDTORequest):
    productos.append(producto)
    return JSONResponse(status_code=201, content={"message": "Producto agregado"})


@router.put("/productos/{id}", tags=["Bodega"])
async def Actualizar_Producto(id: int, producto: productosDTORequest):
    for producto in productos:
        if producto["id"] == id:
            producto["nombre"] = producto.nombre
            producto["categoria"] = producto.categoria
            producto["precio"] = producto.precio
            producto["cantidad"] = producto.cantidad
            return JSONResponse(
                status_code=201, content={"message": "Producto actualizado"}
            )
    return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})


@router.delete("/productos/{id}", tags=["Bodega"])
async def Eliminar_Producto(id: int):
    for producto in productos:
        if producto["id"] == id:
            productos.remove(producto)
            return JSONResponse(
                status_code=200, content={"message": "Producto eliminado"}
            )
    return JSONResponse(status_code=404, content={"message": "Producto no encontrado"})