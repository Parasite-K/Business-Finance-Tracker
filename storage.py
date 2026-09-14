import os

import psycopg

from psycopg.rows import dict_row

from dotenv import load_dotenv
load_dotenv()


def get_connection():
    
    password = os.getenv("DB_PASSWORD")
    return psycopg.connect(dbname="business_expense_tracker",
                        user="postgres",  
                        password = password,
                        host="localhost") 
        

#transactions
def load_transactions():
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM transactions")
            transactions = cur.fetchall()
            return transactions



def save_transaction(txn_type, category, description, date, amount, project_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO transactions(type, category, description, date, amount, project_id) " \
                "VALUES(%s, %s, %s, %s, %s, %s) "
                "RETURNING id",
                (txn_type, category, description, date, amount, project_id )
                )
            result = cur.fetchone()
            return result[0]

def update_transaction(txn_type, category, description, date, amount, project_id, edit_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE transactions " \
                "SET type = %s, " \
                "category = %s, " \
                "description = %s, " \
                "date = %s, " \
                "amount = %s, " \
                "project_id = %s " \
                "WHERE id = %s" ,
                (txn_type, category, description, date, amount, project_id, edit_id)
            )



def delete_transaction(del_id):
    with get_connection() as conn:
        with conn.cursor() as cur: 
            cur.execute(
                "DELETE FROM transactions " \
                "WHERE id = %s",
                (del_id, )
            )


def load_transactions_with_project_names():
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT transactions.* , projects.name as project_name " \
                        "FROM transactions " \
                        "LEFT JOIN projects ON transactions.project_id = projects.id" \
            )
            result = cur.fetchall()
            return result


#===========================================

#Projects

def load_projects():
    with get_connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("SELECT * FROM projects")
            projects = cur.fetchall()
            return projects 



def save_project(project_name, client_id, start_date, end_date, estimated_revenue):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO projects (name, client_id, start_date, end_date, estimated_revenue) " \
                "VALUES(%s, %s, %s, %s, %s) " \
                "RETURNING id",
                (project_name, client_id, start_date, end_date, estimated_revenue)
                )
            result = cur.fetchone()
            return result[0]

def update_project(project_name, start_date, end_date, estimated_revenue, edit_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE projects " \
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

def get_project_stats(project_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*), " \
                        "COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0), " \
                        "COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) " \
                        "FROM transactions " \
                        "WHERE project_id = %s",
                        (project_id, )
            )
            values = cur.fetchone()
            txn_count = values[0] 
            income = values[1] 
            expense = values[2] 

            return txn_count, income, expense

def get_project_transaction_ids(project_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id " \
                        "FROM transactions " \
                        "WHERE project_id = %s",
                        (project_id, )
            )
            res = cur.fetchall()
            txn_ids = [row[0] for row in res]

            return txn_ids
