import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from app.routes.Bodega.BodegaControladores import router as bodega_router
from app.routes.Login.LoginControlador import router as login_router
from app.routes.Usuarios.UsuariosController import router as usuarios_router
from app.routes.Proveedores.ProveedoresController import router as proveedores_router
from app.routes.Categorias.CategoriaController import router as categoria_router
from app.routes.Cliente.ClienteController import router as cliente_router
from app.routes.Pagos.PagosController import router as pagos_router
from app.routes.Historicos.HistoricoController import router as historico_router
from app.routes.CargaExcel.CargaController import router as carga_router
from app.models.Tables import Base
from app.database.Config import engine

Base.metadata.create_all(bind=engine)


app = FastAPI()

# al poner la ruta '/docs' se abre el swagger
app.title = "pyBusiness"
app.version = "0.1.0"


@app.get("/", tags=["Default"])
def main():
    return RedirectResponse("/docs")


origins = {
    "http://localhost:8000",
    "http://localhost:8080",
    "http://localhost:5173",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router, prefix="/login", tags=["Login"])
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(bodega_router, prefix="/bodega", tags=["Bodega"])
app.include_router(proveedores_router, prefix="/proveedores", tags=["Proveedores"])
app.include_router(categoria_router, prefix="/categorias", tags=["Categorias"])
app.include_router(cliente_router, prefix="/clientes", tags=["Clientes"])
app.include_router(pagos_router, prefix="/pagos", tags=["Pagos"])
app.include_router(historico_router, prefix="/historicos", tags=["Historicos"])
app.include_router(carga_router, prefix="/carga", tags=["Cargas masivas"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
