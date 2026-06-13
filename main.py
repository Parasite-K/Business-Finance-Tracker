from datetime import datetime

transactions = []
next_id = 1

#helper functions
def get_valid_date():
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
            return amount 
        except ValueError:
            print("Please enter a valid Number")

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
    pass

def view_transactions(): 
    if not transactions:
        print("No transactions found.")

    for transaction in  transactions:
        print("-" * 30)
        print(f"Transaction ID: #{transaction['id']}")
        print(f"Type: {transaction['type']}")
        print(f"Category: {transaction['category']}")
        print(f"Description: {transaction['description']}")
        print(f"Date: {transaction['date']}")
        print(f"Amount: ₹{transaction['amount']}")
        print("-" * 30)

def main():
    while True:
        choice = input(
        "\n1. Add Transaction"
        "\n2. View Transactions"
        "\n3. Exit"
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
            break

        else:
            print("Invalid choice.")



if __name__ == "__main__":
    main()


        


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    