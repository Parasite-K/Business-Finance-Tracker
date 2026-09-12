
from validation import get_valid_date, get_valid_amount

from storage import (
    save_project , 
    load_projects, 
    update_project, 
    delete_project,
    get_project_stats,
    get_project_transaction_ids
)


def add_project():
    while True:
        project_name = input("Please enter the Name of the Project: ").strip()

        if project_name:
            break

        else:
            print("Project name cannot be empty.")
            continue

    while True:
        print("\nPlease enter the Start Date of the Project.")
        start_date = get_valid_date()
        print("\nPlease enter the End Date of the Project.")
        end_date = get_valid_date()

        if start_date > end_date:
            print("End Date must be after the Start date.")
            continue
        break


    print("\nPlease enter the Estimated Revenue amount of this Project.")
    estimated_revenue = get_valid_amount()

    project_id = save_project(project_name, None, start_date, end_date, estimated_revenue)

    print(f"\nProject '{project_name}' created successfully.")
    print(f"\nProject ID = #{project_id}")
    



  #new
def view_projects():
    projects = load_projects()

    if not projects:
        print("No existing projects available.")
        return

    for project in projects:
        print_project(project)




def del_project():
    projects = load_projects()


    if not projects:
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

    for project in projects:
        if del_id == project["id"]:
            print("=" * 30)
            print_project(project)
            print("=" * 30)

            txn_ids = get_project_transaction_ids(del_id)
            txn_count = len(txn_ids)
            if txn_ids:
                print(f"This project cannot be deleted because it has {txn_count} transactions associated to it.")
                print(f"Associated Transaction IDs: #{', #'.join(str(txn_id) for txn_id in txn_ids)}")
            
                        
      
            confirm = input("\n1. Confirm"
                            "\n2. Cancel"
                            "\n>>  ").strip()
            
            if confirm == "1":
                delete_project(del_id)
                print(f"Project ID: #{project['id']} has been successfully deleted.")
                return

            else:
                print("Not confirmed. Deletion Cancelled.")
                return
    
    print("Project ID could not be found. Please try again.")




def edit_project():
    projects = load_projects()

    if not projects:
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

    for project in projects:
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
                        print("====== EDITING PROJECT NAME ======")
                        edited_project['name'] = input("\nEnter the new project name: ")

                    case "2":
                        print("====== EDITING PROJECT START DATE ======")
                        edited_project['start_date'] = get_valid_date()

                    case "3":
                        print("====== EDITING PROJECT END DATE ======")
                        edited_project['end_date'] = get_valid_date()

                    case "4":
                        print("====== EDITING PROJECT ESTIMATED REVENUE ======")
                        edited_project['estimated_revenue'] = get_valid_amount()

                    case "5":

                        update_project(edited_project["name"], edited_project["start_date"], edited_project["end_date"], edited_project["estimated_revenue"], edit_id)

                        
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
    print(f"Start Date : {project['start_date'].strftime("%d/%m/%Y")}")
    print(f"End Date : {project['end_date'].strftime("%d/%m/%Y")}")
    print(f"Estimated Revenue : ₹{project['estimated_revenue']}")

    txn_count , total_income, total_expense = get_project_stats(project['id'])

    print("------- Financial summary -------")
    
    print(f"Total Transactions: {txn_count}")
    print(f"total Income: ₹{total_income}")
    print(f"Total Expense: ₹{total_expense}")
    print(f"Profit/Loss: ₹{total_income - total_expense}")
    print("=" * 30)



