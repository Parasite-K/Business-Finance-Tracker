
import calendar

from storage import load_transaction, set_next_id

from reports import (
    financial_summary,
    monthly_report,
    yearly_report,
    category_report
)

from transactions import(
    add_transaction,
    del_transaction,
    edit_transaction,
    view_transactions
)


#Reports menu
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
                add_transaction()
                   
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


        


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    