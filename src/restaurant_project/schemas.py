from pydantic import BaseModel, Field, EmailStr, field_validator, BeforeValidator
from typing import Optional, Annotated
from datetime import datetime
from enum import Enum
from string import digits
from .jsondb import Menu_items_base

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

    @field_validator('menu_item_id')
    @classmethod
    def menu_item_id_validate(cls, id):
        if id not in Menu_items_base:
            raise ValueError('uncorrect item id')
        return id

def items_validation(items: list[OrderItem]) -> list[OrderItem]:
    if not (1 <= len(items) <= 20):
        raise ValueError('order size must be between 1 and 20 items')
    
    all_IDs = [item.menu_item_id for item in items]
    if len(set(all_IDs)) != len(items):
        raise ValueError('dublicate menu_item_id in order items')
        
    return items

ItemsType = Annotated[list[OrderItem], BeforeValidator(items_validation)]

class OrderCreate(BaseModel):
    table_number: int = Field(...,ge=1,le=50)
    items: ItemsType
    customer_name: Optional[str] = Field(None, min_length=2)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator('phone')
    @classmethod
    def phone_validation(cls, phone):
        if phone == None: return None
        
        if any(symbol not in f"{digits}-+ "for symbol in phone):
            raise ValueError('uncorrected symbols')
        
        phone = ''.join([symbol for symbol in phone if symbol.isdigit()])

        if phone[0] not in '78':
            raise ValueError('region must be russian (+7 or 8)')
        
        if len(phone) != 11: 
            raise ValueError('uncorrect phone number')
        return f'+7{phone[1:]}'

class OrderStatus(str, Enum):
    PENDING = 'pending'
    PREPARING = 'preparing'
    READY = 'ready'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class Order(BaseModel):
    id: int
    items: ItemsType
    total_price: float 
    tax: float = 10
    discount: Optional[float] = 0
    final_price: float
    status: OrderStatus
    created_at: datetime
    estimated_ready_at: datetime