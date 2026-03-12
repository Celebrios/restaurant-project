from fastapi import FastAPI, HTTPException
from .schemas import *
from .jsondb import Menu_items_base, counters, get_new_menu_item_id, save_db

app = FastAPI()

@app.post('/menu', response_model=MenuItem, status_code=201)
def create_menu_item(item: MenuItemCreate):
    new_name = item.name.lower()
    if any(item['name'] == new_name for item in Menu_items_base.values()):
        raise HTTPException(
            status_code=409, 
            detail=f'item with name {new_name} already exists'
            )
    new_id = get_new_menu_item_id()
    new_menu_item = {
        'id': new_id,
        'name': new_name,
        'description': item.description,
        'price': item.price,
        'category': item.category,
        'is_available': item.is_available,
        'preparation_time': item.preparation_time
    }
    Menu_items_base[new_id] = new_menu_item
    save_db()
    return new_menu_item

@app.get('/menu', response_model=list[MenuItem])
def get_menu(
        category: Optional[Item_category] = None,
        available_only: bool = False
        ):
    if category:
        filtered = []
        for item in Menu_items_base.values():
            if item['category'] == category:
                if available_only and item['is_available']:
                    filtered.append(item)
                    continue
                filtered.append(item)
        return filtered
    return Menu_items_base.values()