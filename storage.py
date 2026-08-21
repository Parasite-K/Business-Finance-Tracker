import json

import data

#transactions
def load_transactions():
    try:
        with open("transactions.json","r") as f:
            data.transactions = json.load(f)
    except FileNotFoundError:
        data.transactions = []


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

#===========================================

#Projects

def load_projects():
    try:
        with open("projects.json" , "r") as f:
            data.projects = json.load(f)
    except FileNotFoundError:
        data.projects = []

def save_projects():
    with open("projects.json", "w") as f:
        json.dump(data.projects, f, indent=4)

def set_next_project_id():
    if not data.projects:
        data.next_project_id = 1 
        return

    else:

        greatest = 0 
        for project in data.projects:
            if project["id"] > greatest:
                greatest = project["id"]
        data.next_project_id = greatest + 1