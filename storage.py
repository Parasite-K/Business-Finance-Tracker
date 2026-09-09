import json

import data

import os

import psycopg

from psycopg.rows import dict_row

from dotenv import load_dotenv
load_dotenv()

from datetime import date


def get_connection():
    
    password = os.getenv("DB_PASSWORD")
    return psycopg.connect(dbname="business_expense_tracker",
                        user="postgres",  
                        password = password,
                        host="localhost") 
        





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
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM projects")
            projects = cur.fetchall()
            return projects 



def save_project(project_name, Client_id, start_date, end_date, estimated_revenue):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO projects (name, client_id, start_date, end_date, estimated_revenue) " \
                "VALUES(%s, %s, %s, %s, %s) " \
                "RETURNING id",
                (project_name, Client_id, start_date, end_date, estimated_revenue)
                )
            result = cur.fetchone()
            return result[0]

def update_project(project_name, start_date, end_date, estimated_revenue, edit_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE Projects " \
                "SET name = %s, " \
                "start_date = %s, " \
                "end_date = %s, " \
                "estimated_revenue = %s " \
                "WHERE id = %s" ,
                (project_name, start_date, end_date, estimated_revenue, edit_id)
            )


def delete_project(project_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM projects " \
                        "WHERE id = %s",
                        (project_id,)
            )

if __name__ == "__main__":
    delete_project(5)
