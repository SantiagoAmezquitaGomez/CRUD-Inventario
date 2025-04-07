# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

# Puedes definir la URI de conexión en una variable de entorno o escribirla directamente.
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://santy:santy1@clustersa.a1wdk.mongodb.net/")

# Crear el cliente y la base de datos
cliente = AsyncIOMotorClient(MONGO_URI)
base_datos = cliente.inventario_tienda

# Definir la colección de items
coleccion_items = base_datos.get_collection("items")