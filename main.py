from datetime import datetime

transactions = []
next_id = 1

#helper functions
def get_valid_date():   #Only accept valid dates.
    while True:
        date = input("Enter the Date (DD/MM/YYYY)")
        
        try:
            datetime.strptime(date, "%d/%m/%Y")
            return date
            
        
        except ValueError:
            print("Invalid Date.")

def get_valid_amount():
      while True:      #To make sure a valid integer is entered.
        amount = input("Enter the Amount:")
        try:
            amount = float(amount)
            if amount < 0:
                print("Amount cannot be negative.")
                continue
            return amount 
        except ValueError:
            print("Please enter a valid Number")

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
                print(f"Transaction : #{transaction['id']} for {transaction['amount']} has been succesfully deleted.")
                return

            else:
                print("Not confirmed. Deletion Cancelled.")
                return
    
    print("Transaction ID could not be found. Please try again.")









def view_transactions(): 
    if not transactions:
        print("No transactions found.")

    for transaction in  transactions:
        print("-" * 30)
        print_transaction(transaction)
        print("-" * 30)

def show_summary():
    total_income = 0
    total_expense = 0

    if not transactions:
        print("\nNo transactions available.")
        return

    for transaction in transactions:
        if transaction["type"] == "income":
            total_income += transaction["amount"]

        elif transaction["type"] == "expense":
            total_expense += transaction["amount"]

    profit = total_income - total_expense 

    print("=" * 30)
    print("SUMMARY FOR ALL TRANSACTIONS:- ")
    print(f"Total Income = +₹{total_income}")
    print(f"Total Expense = -₹{total_expense}")
    print(f"Total Profit = ₹{profit}")
    print("=" * 30)




#main
def main():
    while True:
        choice = input(
        "\n1. Add Transaction"
        "\n2. View Transactions"
        "\n3. Delete a Transaction"
        "\n4. Show summary for all Transactions"
        "\n5. Exit"
        "\n>> "
    )
        
        if choice == "1":
            while True:        #Make sure only Expense or Income is entered.
                txn_type = input("\nSelect transaction type (Expense/Income): ").strip().lower()
                if txn_type in ["expense" , "income"]:
                    add_transaction(transaction_type=txn_type)
                    break
                print("Please enter Expense or Income.")

                    
        elif choice == "2":
            view_transactions()

        elif choice == "3":
            del_transaction()

        elif choice == "4":
            show_summary()

        elif choice == "5":
            break

        else:
            print("Invalid choice.")



if __name__ == "__main__":
    main()


        


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    