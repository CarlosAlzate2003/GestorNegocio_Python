import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from app.routes.Bodega.BodegaControladores import router as bodega_router
from app.routes.Login.LoginControlador import router as login_router


app = FastAPI()

# al poner la ruta '/docs' se abre el swagger
app.title = "GestorNegocio"
app.version = "0.0.1"


@app.get("/", tags=["Default"])
def main():
    return RedirectResponse("/docs")


@app.get("/Home", tags=["Default"])
async def Home():
    return HTMLResponse("<h1>Hello World</h1>")


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
app.include_router(bodega_router, prefix="/bodega", tags=["Bodega"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
