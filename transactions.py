import data
from storage import save_transactions

from validation import(
    get_valid_date,
    get_valid_category,
    get_valid_type,
    get_valid_amount
)


def add_transaction():
    txn_type = get_valid_type()
    date = get_valid_date()
    category = get_valid_category(txn_type)
    description = input("Enter the Description: ")
    amount = get_valid_amount()

    transaction = {
        "id": data.next_id,
        "type": txn_type,
        "category": category,
        "description": description,
        "date": date,
        "amount": amount
    }
    
    data.transactions.append(transaction)
    save_transactions()

    data.next_id += 1 

    print(f"Transaction for ₹{amount} succesfully added!")
    print(f"Transaction id: {transaction["id"]}")


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


def print_transaction(transaction):
    print(f"Transaction ID: #{transaction['id']}")
    print(f"Type: {transaction['type']}")
    print(f"Category: {transaction['category']}")
    print(f"Description: {transaction['description']}")
    print(f"Date: {transaction['date']}")
    print(f"Amount: ₹{transaction['amount']}")