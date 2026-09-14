from storage import get_connection

from validation import(
    get_valid_month,
    get_valid_year,
    get_valid_category,
    get_valid_type
)



def monthly_report():
    query_year = get_valid_year()
    query_month = get_valid_month() 
    

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
            txn_count, income, expenses = result[0], result[1], result[2]
            return txn_count, income, expenses, query_month, query_year




def yearly_report():
    query_year = get_valid_year()
    
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
            return txn_count, income, expenses, query_year




def category_report():

    print("Please select the transaction type of the category you are looking for.")
    txn_type = get_valid_type()
    query_category = get_valid_category(txn_type)
    
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
            return txn_count, total, query_category, txn_type
        



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
