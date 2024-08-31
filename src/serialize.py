import pickle
import json
from copy import copy
import inspect
from datetime import datetime

objToId = {}

def newId(obj):
    newId = len(objToId) + 1
    objToId[obj] = newId
    return newId

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # print(obj.__class__.__name__)
        if isinstance(obj, datetime):
            dct = {'__type': 'datetime', 'time': obj.isoformat()}
            return dct
        
        if obj in objToId:
            dct = {}
            dct['__id'] = objToId[obj]
            return dct
        
        if hasattr(obj, '__dict__'):
            dct = copy(obj.__dict__)
            id = newId(obj)
            dct['__type'] = obj.__class__.__name__
            dct['__id'] = id
            if 'children' in dct:
                dct['children'] = []
            return dct

        return json.JSONEncoder.default(self, obj)

db = pickle.load(open('file.pickle', 'rb'))

def dump(obj, fname):
    with open(fname, 'w') as f:
        json.dump(obj, f, cls=CustomEncoder, indent=2)

dump(db.accounts, 'accounts.json')
dump(db.transactions, 'transactions.json')
dump(db.rules, 'rules.json')
