import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
STATE_FILE = BASE_DIR / 'state.json'


def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)            
    except FileNotFoundError:              
        return {
            'users':{},
            'counters': {
                'max_user_id': 0
            },
            'menu_items_by_id':{},
            'menu_items_by_name':{}
        }

def save_db():
    with open(STATE_FILE, 'w') as f:      
        json.dump(db, f, indent=4)   

db = load_state()
# db['MenuItemsByName'] = {} ---> in development
Menu_items_base = db['menu_items_by_id']
# Menu_items_base_by_name = db['MenuItemsByName'] ---> in development
counters = db['counters']
save_db()

def get_new_user_id():
    counters['max_user_id'] += 1
    save_db()
    return counters['max_user_id']



