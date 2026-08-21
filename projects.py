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