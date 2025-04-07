# app/main.py
from fastapi import FastAPI
from app.routes import item_routes

app = FastAPI(
    title="API de Inventario de Tienda de Tecnología",
    description="API CRUD para gestionar el inventario de una tienda de tecnología (celulares, portátiles, tablets).",
    version="1.0.0"
)

# Incluir las rutas de items con el prefijo /items
app.include_router(item_routes.router, prefix="/items", tags=["Items"])
    