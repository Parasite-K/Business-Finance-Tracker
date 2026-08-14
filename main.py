import json
import calendar

from datetime import datetime

#helper functions

def set_next_id():            
    global next_id

    if not transactions:
        next_id = 1
        return
        
    else:
    
        greatest = 0
        for transaction in transactions:
            if transaction["id"] > greatest:
                greatest = transaction["id"]
        next_id = greatest + 1




def save_transactions():
    with open ("transactions.json" , "w") as f:
        json.dump(transactions, f , indent=4)

def get_valid_month():
    while True:
        query_month = input("Enter the month number(1-12): ")
        try:
            query_month = int(query_month)
            if 1 <= query_month <= 12:
                return query_month
            else:
                print("Not a valid month (Must be between 1 - 12)")
        except ValueError:
            print("Enter a valid month number.")

def get_valid_year():
    while True:
        query_year = input("Enter the Year:")
        try:
            query_year = int(query_year)
            if 1<= query_year <= 9999:
                return query_year
            else:
                print("Not a valid Year.")
        except ValueError:
            print("Enter a valid Year.")

def get_month_year(date):
    _, month, year = date.split("/")
    return int(month), int(year)



def get_valid_date():   
    while True:
        date = input("Enter the Date (DD/MM/YYYY): ")
        
        try:
            datetime.strptime(date, "%d/%m/%Y")
            return date
            
        
        except ValueError:
            print("Invalid Date.")

def get_valid_amount():
      while True:     
        amount = input("Enter the Amount: ₹")
        try:
            amount = float(amount)
            if amount < 0:
                print("Amount cannot be negative.")
                continue
            return amount 
        except ValueError:
            print("Please enter a valid Number")


def get_valid_type():                       
    while True:        
        txn_type = input("\nSelect transaction type (Expense/Income): ").strip().lower()
        if txn_type in ["expense" , "income"]:
            return txn_type
        else:
            print("Please enter either Expense or Income.")
            continue




def print_transaction(transaction):
    print(f"Transaction ID: #{transaction['id']}")
    print(f"Type: {transaction['type']}")
    print(f"Category: {transaction['category']}")
    print(f"Description: {transaction['description']}")
    print(f"Date: {transaction['date']}")
    print(f"Amount: ₹{transaction['amount']}")




#Core functions

def add_transaction(transaction_type):
    global next_id

    date = get_valid_date()
    category = input("Enter the Category: ")
    description = input("Enter the Description: ")
    amount = get_valid_amount()

    transaction = {
        "id": next_id,
        "type": transaction_type,
        "category": category,
        "description": description,
        "date": date,
        "amount": amount
    }
    
    transactions.append(transaction)
    save_transactions()

    next_id += 1 

    print("Transaction added successfully!")


def del_transaction():
    if not transactions:
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

    for transaction in transactions:
        if del_id == transaction["id"]:
            print("=" * 30)
            print_transaction(transaction)
            print("=" * 30)
            confirm = input("\n1. Confirm"
                            "\n2. Cancel"
                            "\n>>  ").strip()
            
            if confirm == "1":
                transactions.remove(transaction)
                print(f"Transaction : #{transaction['id']} for ₹{transaction['amount']} has been succesfully deleted.")
                return

            else:
                print("Not confirmed. Deletion Cancelled.")
                return
    
    print("Transaction ID could not be found. Please try again.")



def edit_transaction():
    if not transactions:
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

    for transaction in transactions:
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
                        edited_transaction["type"] = get_valid_type()

                    case "3":
                        edited_transaction["category"] = input("Enter the category: ")

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
    if not transactions:
        print("No transactions found.")

    for transaction in  transactions:
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

    if not transactions:
        print("No transactions available.")

    for transaction in transactions:
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

    if not transactions:
        print("\nNo transactions available.")
        return

    for transaction in transactions:
        _, txn_year = get_month_year(transaction["date"])
        if query_year == txn_year:
            txn_count += 1

            if transaction["type"] == "income":
                income += transaction["amount"]
            else:
                expenses += transaction["amount"]

    return txn_count, income, expenses, query_year


def financial_summary():
    total_income = 0
    total_expense = 0
    txn_count = 0 

    if not transactions:
        print("\nNo transactions available.")
        return

    for transaction in transactions:
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
                print("Coming soon...")

            case "5":
                return

            case _:
                print("Invalid choice.")





def load_transaction():
    global transactions
    try:
        with open("transactions.json","r") as f:
            transactions = json.load(f)
    except FileNotFoundError:
        transactions = []


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


        


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    