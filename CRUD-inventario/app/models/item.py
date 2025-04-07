# app/models/item.py
from pydantic import BaseModel, Field
from typing import Optional

class ItemBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    categoria: str  # Ej: "celular", "portátil", "tablet"
    precio: float
    cantidad: int

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: str

    class Config:
        orm_mode = True