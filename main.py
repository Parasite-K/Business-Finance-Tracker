import json
import calendar

from datetime import datetime

from validation import (
    get_valid_date,
    get_valid_month,
    get_valid_year,
    get_month_year,
    get_valid_amount,
    get_valid_type,
    get_valid_category
)

from storage import save_transactions, load_transaction, set_next_id

import data

from transactions import(
    add_transaction,
    del_transaction,
    edit_transaction,
    view_transactions
)

categories = {
    "income": [
        "Sales",
        "Services",
        "Other Income"
    ],
    "expense": [
        "Materials",
        "Salary",
        "Rent",
        "Utilities",
        "Fuel",
        "Marketing",
        "Equipment",
        "Travel",
        "Miscellaneous"
    ]
}





#CORE REPORT FUNCTIONS:-
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


def reports_menu():
    while True:
        print("\n======REPORTS======")
        choice = input(
            "\n1. Financial Summary"
            "\n2. Monthly Report"
            "\n3. Yearly Report"
            "\n4. Category based report"
            "\n5. Back"
            "\n>> ").strip()

        match choice:
            case "1":
                txn_count, income, expenses = financial_summary()

                print("\n===== FINANCIAL SUMMARY =====")
                print(f"Number of Transactions: {txn_count}")
                print(f"Total Income: ₹{income}")
                print(f"Total Expenses: ₹{expenses}")
                print(f"Profit/Loss: ₹{income - expenses}")

            case "2":
                txn_count, income, expenses, query_month, query_year = monthly_report()
                month_name = calendar.month_name[query_month]

                print(f"\n===== MONTHLY REPORT for {month_name} {query_year} =====")
                print(f"Transactions: {txn_count}")
                print(f"Income: ₹{income}")
                print(f"Expenses: ₹{expenses}")
                print(f"Profit/Loss: ₹{income - expenses}")

            case "3":
                txn_count, income, expenses, query_year = yearly_report()

                print(f"\n===== YEARLY REPORT for {query_year} =====")
                print(f"Transactions: {txn_count}")
                print(f"Income: ₹{income}")
                print(f"Expenses: ₹{expenses}")
                print(f"Profit/Loss: ₹{income - expenses}")

            case "4":
                txn_count, total, query_category, txn_type = category_report()

                print(f"\n===== CATEGORY REPORT: {query_category} =====")
                print(f"Type: {txn_type.title()}")
                print(f"Transactions: {txn_count}")
                print(f"Total {txn_type.title()}: ₹{total}")


            case "5":
                return

            case _:
                print("Invalid choice.")





#main
def main():
    while True:
        choice = input(
        "\n1. Add Transaction"
        "\n2. View Transactions"
        "\n3. Delete a Transaction"
        "\n4. Edit a transaction"
        "\n5. View Reports"
        "\n6. Exit"
        "\n>> "
    ).strip()
        match choice:

            case "1":
                txn_type = get_valid_type()
                add_transaction(txn_type)
                   
            case "2":
                view_transactions()

            case "3":
                del_transaction()

            case "4":
                edit_transaction()

            case "5":
                reports_menu()

            case "6":
                return

            case _:
                print("Invalid choice.")


if __name__ == "__main__":
    load_transaction()
    set_next_id()
    main()


        


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    