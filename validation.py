from datetime import datetime

from data import categories


def get_valid_date():   
    while True:
        date = input("Enter the Date (DD/MM/YYYY): ")
        
        try:
            datetime.strptime(date, "%d/%m/%Y")
            return date
            
        
        except ValueError:
            print("Invalid Date.")

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

def get_valid_category(txn_type):
    category_list = categories[txn_type]

    while True:
        print("\nSelect your category:")

        for i , category in enumerate(category_list, 1):
            print(f"{i}. {category}")
        choice = input(">> ").strip()

        try:
            choice = int(choice)
            if 1 <= choice <= len(category_list):
                return category_list[choice - 1]

            else:
                print("Please choose a valid Category.")
        except:
            print("Please enter a category number.")