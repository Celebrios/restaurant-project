import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
STATE_FILE = BASE_DIR / 'state.json'


def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
            data['orders'] = {int(k): v for k, v in data['orders'].items()}
            data['menu_items_by_id'] = {int(k): v for k, v in data['menu_items_by_id'].items()}
            return data
    except FileNotFoundError:              
        return {
            'users': {},
            'counters': {
                'max_user_id': 0,
                'max_menu_item_id': 0,
                'max_order_id': 0
            },
            'menu_items_by_id': {},
            'menu_items_by_name': {},
            'promocodes': {},
            'orders': {}
        }

def save_db():
    with open(STATE_FILE, 'w') as f:      
        json.dump(db, f, indent=4)   

db = load_state()
# db['MenuItemsByName'] = {} ---> in development
Menu_items_base = db['menu_items_by_id']
# Menu_items_base_by_name = db['MenuItemsByName'] ---> in development
counters = db['counters']
orders = db['orders']
save_db()

def get_new_user_id():
    counters['max_user_id'] += 1
    save_db()
    return counters['max_user_id']

def get_new_menu_item_id():
    counters['max_menu_item_id'] += 1
    save_db()
    return counters['max_menu_item_id']

def get_new_order_id():
    counters['max_order_id'] += 1
    save_db()
    return counters['max_order_id']

def check_promo(promocode):
    if promocode in db['promocodes']:
        return db['promocodes'][promocode]
    return 0

def get_menu_item(id):
    return Menu_items_base[id]

def get_menu_items():
    return Menu_items_base.values()

def add_item_to_menu(id,item):
    Menu_items_base[id] = item
    save_db()
    return 'successful'

def add_new_order(id,order):
    orders[id] = order
    save_db()
    return 'successful'

def get_order(id):
    return orders[id]