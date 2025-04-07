# app/routes/item_routes.py
from fastapi import APIRouter, HTTPException, status
from app.models.item import ItemCreate, Item
from app.database import coleccion_items
from bson import ObjectId

router = APIRouter()

# Función auxiliar para convertir el documento MongoDB a un diccionario
def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "nombre": item["nombre"],
        "descripcion": item.get("descripcion"),
        "categoria": item["categoria"],
        "precio": item["precio"],
        "cantidad": item["cantidad"]
    }

# Endpoint: Crear un recurso (POST /items/)
@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def crear_item(item: ItemCreate):
    item_dict = item.dict()
    resultado = await coleccion_items.insert_one(item_dict)
    nuevo_item = await coleccion_items.find_one({"_id": resultado.inserted_id})
    if nuevo_item:
        return item_helper(nuevo_item)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error al crear el item")

# Endpoint: Leer un recurso específico (GET /items/{id})
@router.get("/{id}", response_model=Item)
async def obtener_item_ID(id: str):
    item = await coleccion_items.find_one({"_id": ObjectId(id)})
    if item:
        return item_helper(item)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

# Endpoint: Leer todos los recursos (GET /items/)
@router.get("/", response_model=list[Item])
async def obtener_items():
    items = []
    async for item in coleccion_items.find():
        items.append(item_helper(item))
    return items

# Endpoint: Actualizar un recurso (PUT /items/{id})
@router.put("/{id}", response_model=Item)
async def actualizar_item(id: str, item: ItemCreate):
    item_actualizado = item.dict()
    resultado = await coleccion_items.update_one({"_id": ObjectId(id)}, {"$set": item_actualizado})
    if resultado.modified_count == 1:
        item_modificado = await coleccion_items.find_one({"_id": ObjectId(id)})
        if item_modificado:
            return item_helper(item_modificado)
    # Si no se modificó pero existe, se devuelve el item existente
    item_existente = await coleccion_items.find_one({"_id": ObjectId(id)})
    if item_existente:
        return item_helper(item_existente)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")

# Endpoint: Eliminar un recurso (DELETE /items/{id})
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_item(id: str):
    resultado = await coleccion_items.delete_one({"_id": ObjectId(id)})
    if resultado.deleted_count == 1:
        return {"mensaje": "Item eliminado correctamente"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado")
