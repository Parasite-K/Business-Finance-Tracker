import data

from validation import(
    get_valid_month,
    get_valid_year,
    get_month_year,
    get_valid_category,
    get_valid_type
)



def monthly_report():
    query_month = get_valid_month()
    query_year = get_valid_year()
    txn_count = 0
    income = 0
    expenses = 0 

    if not data.transactions:
        print("No transactions available.")

    for transaction in data.transactions:
        txn_month , txn_year = get_month_year(transaction["date"])
        if query_month == txn_month and query_year == txn_year:
            txn_count += 1

            if transaction["type"] == "income":
                income += transaction["amount"]
            else:
                expenses += transaction["amount"]

    return txn_count, income, expenses, query_month, query_year

def yearly_report():
    query_year = get_valid_year()
    txn_count = 0
    income = 0 
    expenses = 0 

    if not data.transactions:
        print("\nNo transactions available.")
        return

    for transaction in data.transactions:
        _, txn_year = get_month_year(transaction["date"])
        if query_year == txn_year:
            txn_count += 1

            if transaction["type"] == "income":
                income += transaction["amount"]
            else:
                expenses += transaction["amount"]

    return txn_count, income, expenses, query_year

def category_report():
    txn_count = 0
    total = 0 

    if not data.transactions:
            print("\nNo transactions available.")
            return

    print("Please select the transaction type of the category you are looking for.")
    txn_type = get_valid_type()
    query_category = get_valid_category(txn_type)

    for transaction in data.transactions:
        if transaction["category"] == query_category:
            txn_count += 1 
            total += transaction["amount"]


    return txn_count, total, query_category, txn_type


def financial_summary():
    total_income = 0
    total_expense = 0
    txn_count = 0 

    if not data.transactions:
        print("\nNo transactions available.")
        return

    for transaction in data.transactions:
        txn_count += 1
        if transaction["type"] == "income":
            total_income += transaction["amount"]

        elif transaction["type"] == "expense":
            total_expense += transaction["amount"]

    return txn_count, total_income, total_expense
