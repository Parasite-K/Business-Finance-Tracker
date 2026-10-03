from storage import get_connection


def monthly_report(query_year, query_month):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*), " \
                        "COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0), " \
                        "COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) " \
                        "FROM transactions " \
                        "WHERE EXTRACT(YEAR FROM date) = %s " \
                        "AND EXTRACT(MONTH FROM date) = %s",
                        (query_year, query_month)
            )
            result = cur.fetchone()
            txn_count, income, expense = result[0], result[1], result[2]
            return txn_count, income, expense




def yearly_report(query_year):  
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*), " \
                        "COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0), " \
                        "COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) " \
                        "FROM transactions " \
                        "WHERE EXTRACT(YEAR FROM date) = %s ",
                        (query_year, )
            )
            result = cur.fetchone()
            txn_count, income, expenses = result[0], result[1], result[2]
            return txn_count, income, expenses




def category_report(txn_type, query_category):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*), " \
                        "COALESCE(SUM(amount) ,0) " \
                        "FROM transactions " \
                        "WHERE category = %s " \
                        "AND type = %s",
                        (query_category, txn_type)
            )
            result = cur.fetchone()
            txn_count, total = result[0], result[1]
            return txn_count, total, 
        


def financial_summary():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*), " \
                        "COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0), " \
                        "COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) " \
                        "FROM transactions"
            )
            result = cur.fetchone()
            txn_count, total_income, total_expense = result[0], result[1], result[2]
            return txn_count, total_income, total_expense
