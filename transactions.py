import data
from storage import save_transactions

from validation import(
    get_valid_date,
    get_valid_category,
    get_valid_type,
    get_valid_amount
)

from projects import view_projects

def add_transaction():
    txn_type = get_valid_type()
    date = get_valid_date()
    category = get_valid_category(txn_type)
    description = input("Enter the Description: ")
    amount = get_valid_amount()
    project_id = get_project_assignment()

    transaction = {
        "id": data.next_id,
        "type": txn_type,
        "category": category,
        "description": description,
        "date": date,
        "amount": amount,
        "project_id": project_id
    }
    
    data.transactions.append(transaction)
    data.next_id += 1
    save_transactions()


    print(f"Transaction for ₹{amount} succesfully added!")
    print(f"Transaction id: #{transaction["id"]}")


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
        edit_id = input("ENTER TRANSACTION ID FOR THE TRANSACTION YOU WANT TO EDIT: #")
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
                             "\n6. Project"
                             "\n7. Save and Exit "
                             "\n8. Exit without saving "
                             "\n>> ").strip()

                

                match choice:
                    case "1":
                        print("====== EDITING DATE ======\n")
                        edited_transaction["date"] = get_valid_date()

                    case "2":
                        print("====== EDITING TYPE ======\n")
                        new_type = get_valid_type()
                        edited_transaction["type"] = new_type
                        print(f"Please Select a category for your new transaction type: {new_type}")

                        edited_transaction["category"] = get_valid_category(new_type)

                    case "3":
                        print("====== EDITING CATEGORY ======\n")
                        edited_transaction["category"] = get_valid_category(edited_transaction["type"])

                    case "4":
                        print("====== EDITING DESCRIPTION ======\n")
                        edited_transaction["description"] = input("Enter a Description: ")

                    case "5": 
                        print("====== EDITING AMOUNT ======")
                        edited_transaction["amount"] = get_valid_amount()

                    case "6":
                        print("====== EDITING PROJECT ======")
                        edited_transaction["project_id"] = get_project_assignment()

                    case "7":
                        transaction.update(edited_transaction)
                        save_transactions()


                        print("The new edited transaction is:-")
                        print("=" * 30)
                        print_transaction(edited_transaction)
                        print("=" * 30)

                        return

                
                    case "8":
                        return

                    case _:
                        print("Invalid choice.")
    print("Transaction not found.")



def view_transactions(): 
    if not data.transactions:
        print("No transactions found.")
        return

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

    project_id = transaction["project_id"]

    if project_id is None:
        print("Project: Not assigned")
    else:
        print(f"Project ID: #{project_id}")
        
    project_name = get_project_name(transaction)
    if project_name:
        print(f"Project Name: {project_name}")
    else:
        print("Project Name: Not assigned")


#transaction - project relationship

def get_project_name(transaction):
    project_id = transaction["project_id"]
    if project_id is None:
        return None
        
    for project in data.projects:
        if project_id == project["id"]:
            return project["name"]
    return None





def get_project_assignment():
    if not data.projects:
        print("No projects are available so Transaction will not be assigned to any.")
        return None

    while True:
        choice = input("Please choose if you want to assign this transaction to a project."
                   "\ny/n >> ").strip().lower()

        if choice == "y":
            view_projects()
            project_id = input("\n Please Select The Project ID: ").strip()

            try:
                project_id = int(project_id)
                for project in data.projects:
                    if project_id == project["id"]:
                        return project_id

                print("Project does not exist.")

            except ValueError:
                print("Project ID must be a number.")
                continue

        elif choice == "n":
            return None

        else:
            print("Invalid input. Please try again.")

    