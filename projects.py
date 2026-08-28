import data
from validation import get_valid_date, get_valid_amount
from storage import save_projects


def add_project():
    while True:
        project_name = input("Please enter the Name of the Project: ").strip()

        if project_name:
            break

        else:
            print("Project name cannot be empty.")
            continue

    print("\nPlease enter the Start Date of the Project.")
    start_date = get_valid_date()
    print("\nPlease enter the End Date of the Project.")
    end_date = get_valid_date()

    print("\nPlease enter the Estimated Revenue amount of this Project.")
    estimated_revenue = get_valid_amount()

    project = {
        "id" : data.next_project_id,
        "name" : project_name,
        "client_id" : None,
        "start_date" : start_date,
        "end_date" : end_date,
        "estimated_revenue" : estimated_revenue,

    }

    data.projects.append(project)
    data.next_project_id += 1
    save_projects()

    print(f"\nProject '{project_name}' created successfully.")
    print(f"Project ID: {project['id']}")

def view_projects():
    if not data.projects:
        print("No existing projects available.")
        return

    for project in data.projects:
        print("=" * 30)
        print_project(project)
        print("=" * 30)

def del_project():
    if not data.projects:
        print("No projects available.")
        return

    view_projects()
    while True:
        del_id = input("ENTER PROJECT ID FOR THE PROJECT YOU WANT TO DELETE: #")
        try:
            del_id = int(del_id)
            break
        except ValueError:
            print("Enter a Valid Project ID.")
            continue

    for project in data.projects:
        if del_id == project["id"]:
            print("=" * 30)
            print_project(project)
            print("=" * 30)

            txn_count , txn_ids  = get_project_transaction_ids(del_id)
            if txn_count >= 1 :
                print(f"This project cannot be deleted because it has {txn_count} transactions associated to it.")
                print(f"Associated Transaction Ids: {txn_ids}")
                return
                        
      
            confirm = input("\n1. Confirm"
                            "\n2. Cancel"
                            "\n>>  ").strip()
            
            if confirm == "1":
                data.projects.remove(project)
                save_projects()
                print(f"Project ID: #{project['id']} has been successfully deleted.")
                return

            else:
                print("Not confirmed. Deletion Cancelled.")
                return
    
    print("Project ID could not be found. Please try again.")


def get_project_transaction_ids(project_id):
    txn_ids = []

    if not data.transactions:
        return len(txn_ids), txn_ids

    for transaction in data.transactions:
        if transaction["project_id"] == project_id:
            txn_ids.append(transaction["id"])

    return len(txn_ids), txn_ids






def edit_project():
    if not data.projects:
        print("No projects available.")
        return
    
    view_projects()
  
    while True:
        edit_id = input("ENTER PROJECT ID FOR THE PROJECT YOU WANT TO EDIT: #")
        try:
            edit_id = int(edit_id)
            break
        except ValueError:
            print("Enter a Valid Project ID.")
            continue

    for project in data.projects:
        if edit_id == project["id"]:
            
            edited_project = project.copy()

            while True:
                print("=" * 30)
                print_project(edited_project)
                print("=" * 30)

                print("\n Choose one of the following:- ")
                choice = input("\n1. Name"
                             "\n2. Start Date"
                             "\n3. End Date"
                             "\n4. Estimated Revenue"
                             "\n5. Save and Exit "
                             "\n6. Exit without saving "
                             "\n>> ").strip()

                match choice:
                    case "1":
                        edited_project['name'] = input("\nEnter the new project name: ")

                    case "2":
                        print("\nEditing START DATE:-")
                        edited_project['start_date'] = get_valid_date()

                    case "3":
                        print("\nEditing END DATE:-")
                        edited_project['end_date'] = get_valid_date()

                    case "4":
                        edited_project['estimated_revenue'] = get_valid_amount()

                    case "5":
                        project.update(edited_project)
                        save_projects()
                        
                        
                        print("The new edited project is:-")
                        print("=" * 30)
                        print_project(edited_project)
                        print("=" * 30)
                        
                        return

                    case "6":
                        return
    print("Project not found.")



def print_project(project):
    print("=" * 30)
    print(f"Project ID: #{project['id']}")
    print(f"Project Name : {project['name']}")
    #print(f"Client ID : {project['']}")
    print(f"Start Date : {project['start_date']}")
    print(f"End Date : {project['end_date']}")
    print(f"Estimated Revenue : ₹{project['estimated_revenue']}")

    txn_count , total_income, total_expense = get_project_stats(project['id'])

    print("------- Financial summary -------")
    
    print(f"Total Transactions: {txn_count}")
    print(f"total Income: ₹{total_income}")
    print(f"Total Expense: ₹{total_expense}")
    print(f"Profit/Loss: ₹{total_income - total_expense}")
    print("=" * 30)

def get_project_stats(project_id):
    txn_count = 0
    income = 0 
    expense = 0 

    for transaction in data.transactions:
        if transaction["project_id"] == project_id:
            if transaction["type"] == "income":
                income += transaction["amount"]
            else:
                expense += transaction["amount"]

            txn_count += 1

    return txn_count, income, expense


            