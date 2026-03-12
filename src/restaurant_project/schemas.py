from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from string import digits
from .jsondb import get_menu_item, get_menu_items

TAX = 10

class Item_category(str, Enum):
    STARTERS = 'starters'
    MAIN = 'main'
    DESSERTS = 'desserts'
    DRINKS = 'drinks'

class MenuItemCreate(BaseModel):
    name: str = Field(...,min_length=3,max_length=100)
    description: Optional[str] = None
    price: float = Field(...,gt=0)
    category: Item_category
    is_available: bool = True
    preparation_time: int = Field(...,ge=5,le=60)

class MenuItem(MenuItemCreate):
    id: int

class OrderItem(BaseModel):
    menu_item_id: int
    quantity: int = Field(...,ge=1, le=10)
    special_instructions: Optional[str] = Field(None, max_length=200)

    @field_validator('menu_item_id')
    @classmethod
    def menu_item_id_validate(cls, id):
        if id not in get_menu_items():
            raise ValueError('uncorrect item id')
        return id

def ValidateItems(items: list[OrderItem]) -> list[OrderItem]:
    if not (1 <= len(items) <= 20):
        raise ValueError('order size must be between 1 and 20 items')
    
    ids = [item.menu_item_id for item in items]
    if len(set(ids)) != len(ids):
        raise ValueError('duplicate menu_item_id')
    
    for item in items:
        menu_item = get_menu_item(item.menu_item_id)
        if not menu_item['is_available']:
            raise ValueError(f"dish {menu_item['name']} is not available")
    
    return items

class OrderCreate(BaseModel):
    table_number: int = Field(...,ge=1,le=50)
    items: list[OrderItem]
    customer_name: Optional[str] = Field(None, min_length=2)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    promocode: Optional[str] = None

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
    
    @field_validator('items')
    @classmethod
    def validate_items(cls, items):
        return ValidateItems(items)

class OrderStatus(str, Enum):
    PENDING = 'pending'
    PREPARING = 'preparing'
    READY = 'ready'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class OrderResponse(OrderCreate):
    id: int
    total_price: float 
    tax: float = TAX
    discount: Optional[float] = 0
    final_price: float
    status: OrderStatus
    created_at: datetime
    estimated_ready_at: datetime