import json

import data


def load_transaction():
    try:
        with open("transactions.json","r") as f:
            data.transactions = json.load(f)
    except FileNotFoundError:
        transactions = []


def save_transactions():
    with open ("transactions.json" , "w") as f:
        json.dump(data.transactions, f , indent=4)

def set_next_id():            
    if not data.transactions:
        data.next_id = 1
        return
        
    else:
    
        greatest = 0
        for transaction in data.transactions:
            if transaction["id"] > greatest:
                greatest = transaction["id"]
        data.next_id = greatest + 1