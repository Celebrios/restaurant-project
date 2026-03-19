from fastapi import FastAPI, HTTPException
from .schemas import *
from . import jsondb
from datetime import timedelta

app = FastAPI()

@app.post('/menu', response_model=MenuItem, status_code=201)
def create_menu_item(item: MenuItemCreate):
    new_name = item.name.lower()
    if any(item['name'] == new_name for item in jsondb.get_menu_items()):
        raise HTTPException(
            status_code=409, 
            detail=f'item with name {new_name} already exists'
            )
    new_id = jsondb.get_new_menu_item_id()
    new_menu_item = {
        'id': new_id,
        'name': new_name,
        'description': item.description,
        'price': item.price,
        'category': item.category,
        'is_available': item.is_available,
        'preparation_time': item.preparation_time
    }
    jsondb.add_item_to_menu(id=new_id, item=new_menu_item)
    return new_menu_item

@app.get('/menu', response_model=list[MenuItem])
def get_menu(
        category: Optional[Item_category] = None,
        available_only: bool = False
        ):
    if category:
        filtered = []
        for item in jsondb.get_menu_items():
            if item['category'] != category:
                continue
            if available_only and not item['is_available']:
                continue
            filtered.append(item)
        return filtered

    if available_only:
        return [item for item in jsondb.get_menu_items() if item['is_available']]

    return jsondb.get_menu_items()

@app.post('/orders', response_model=OrderResponse, status_code=201)
def create_order(order: OrderCreate):
    total_price = 0
    for item in order.items:
        total_price += item.quantity * get_menu_item(item.menu_item_id)['price']

    tax = (total_price/100) * TAX
    discount = (total_price/100) * jsondb.check_promo(order.promocode)
    final_price = total_price + tax - discount

    now = datetime.now()
    estimated_ready_at = now
    for item in order.items:
        preparation_time = get_menu_item(item.menu_item_id)['preparation_time']
        estimated_ready_at += timedelta(minutes= preparation_time*item.quantity)

    new_id = jsondb.get_new_order_id()

    new_order = {
        'id': new_id,
        'table_number': order.table_number,
        'items': [item.model_dump() for item in order.items],
        'customer_name': order.customer_name,
        'phone': order.phone,
        'email': order.email,
        'total_price': total_price,
        'tax': tax,
        'discount': discount,
        'final_price': final_price,
        'status': OrderStatus.PENDING,
        'created_at': now,
        'estimated_ready_at': estimated_ready_at
    }
    return new_order