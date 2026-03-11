import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
STATE_FILE = BASE_DIR / 'state.json'


def load_state():
    try:
        with open(STATE_FILE, 'r') as f:
            return json.load(f)            
    except FileNotFoundError:              
        return {}

def save_db():
    with open(STATE_FILE, 'w') as f:      
        json.dump(db, f, indent=4)   

db = load_state()
db['users'] = {}
db['counters'] = {'max_user_id': 0}
counters = db['counters']
save_db()

def get_new_user_id():
    counters['max_user_id'] += 1
    save_db()
    return counters['max_user_id']



