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

#helper fu




def print_transaction(transaction):
    print(f"Transaction ID: #{transaction['id']}")
    print(f"Type: {transaction['type']}")
    print(f"Category: {transaction['category']}")
    print(f"Description: {transaction['description']}")
    print(f"Date: {transaction['date']}")
    print(f"Amount: ₹{transaction['amount']}")




#Core functions

def add_transaction(transaction_type):

    date = get_valid_date()
    category = get_valid_category(transaction_type)
    description = input("Enter the Description: ")
    amount = get_valid_amount()

    transaction = {
        "id": data.next_id,
        "type": transaction_type,
        "category": category,
        "description": description,
        "date": date,
        "amount": amount
    }
    
    data.transactions.append(transaction)
    save_transactions()

    data.next_id += 1 

    print("Transaction added successfully!")


def del_transaction():
    if not data.transactions:
        print("No transactions available.")
        return

    view_transactions()
    while True:
        del_id = input("ENTER TRANSACTION ID FOR THE TRANSACTION YOU WANT TO DELETE: ")
        try:
            del_id = int(del_id)
            break
        except ValueError:
            print("Enter a Valid Transaction ID.")
            continue

    for transaction in data.transactions:
        if del_id == transaction["id"]:
            print("=" * 30)
            print_transaction(transaction)
            print("=" * 30)
            confirm = input("\n1. Confirm"
                            "\n2. Cancel"
                            "\n>>  ").strip()
            
            if confirm == "1":
                data.transactions.remove(transaction)
                save_transactions()
                print(f"Transaction : #{transaction['id']} for ₹{transaction['amount']} has been succesfully deleted.")
                return

            else:
                print("Not confirmed. Deletion Cancelled.")
                return
    
    print("Transaction ID could not be found. Please try again.")



def edit_transaction():
    if not data.transactions:
        print("No transactions available.")
        return
    
    view_transactions()

    
    while True:
        edit_id = input("ENTER TRANSACTION ID FOR THE TRANSACTION YOU WANT TO EDIT: ")
        try:
            edit_id = int(edit_id)
            break
        except ValueError:
            print("Enter a Valid Transaction ID.")
            continue

    for transaction in data.transactions:
        if edit_id == transaction["id"]:
            

            edited_transaction = transaction.copy()

            while True:
                print("=" * 30)
                print_transaction(edited_transaction)
                print("=" * 30)

                print("\n Choose one of the following:- \n ")
                choice = input("\n1. Date"
                             "\n2. Type"
                             "\n3. Category"
                             "\n4. Description"
                             "\n5. Amount "
                             "\n6. Save and Exit "
                             "\n7. Exit without saving "
                             "\n>> ").strip()

                

                match choice:
                    case "1":
                        edited_transaction["date"] = get_valid_date()

                    case "2":
                        new_type = get_valid_type()
                        edited_transaction["type"] = new_type
                        print(f"Please Select a category for your new transaction type: {new_type}")

                        edited_transaction["category"] = get_valid_category(new_type)

                    case "3":
                        edited_transaction["category"] = get_valid_category(edited_transaction["type"])

                    case "4":
                        edited_transaction["description"] = input("Enter a Description: ")

                    case "5": 
                        edited_transaction["amount"] = get_valid_amount()

                    case "6":
                        transaction.update(edited_transaction)
                        save_transactions()


                        print("The new edited transaction is:-")
                        print("=" * 30)
                        print_transaction(edited_transaction)
                        print("=" * 30)

                        return

                        
                        

                    case "7":
                        return

                    case _:
                        print("Invalid choice.")
    print("Transaction not found.")
                        
                        
                    

def view_transactions(): 
    if not data.transactions:
        print("No transactions found.")

    for transaction in  data.transactions:
        print("-" * 30)
        print_transaction(transaction)
        print("-" * 30)

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


        


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    