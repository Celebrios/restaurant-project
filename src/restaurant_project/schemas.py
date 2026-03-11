from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Item_category(str, Enum):
    STARTERS = 'starters'
    MAIN = 'main'
    DESSERTS = 'desserts'
    DRINKS = 'drinks'


class MenuItem(BaseModel):
    id: int
    name: str = Field(...,min_length=3,max_length=100)
    description: Optional[str] = None
    price: float = Field(...,gt=0)
    category: Item_category
    is_available: bool = True
    preparation_time: int = Field(...,ge=5,le=60)

class OrderItem(BaseModel):
    menu_item_id: int
    quantity: int = Field(...,ge=1, le=10)
    special_instructions: Optional[str] = Field(None, max_length=200)
