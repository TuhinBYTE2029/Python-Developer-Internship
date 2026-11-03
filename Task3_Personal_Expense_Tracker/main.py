"""Command-line interface for the Personal Expense Tracker."""

from expense_manager import ExpenseManager


def show_expenses(manager):
    expenses = manager.list_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print("\nID       DATE        TITLE                 CATEGORY        AMOUNT")
    print("-" * 72)
    for item in expenses:
        print(
            f"{item['id']:<8} {item['date']:<11} "
            f"{item['title'][:20]:<21} {item['category'][:14]:<15} "
            f"₹{item['amount']:>9.2f}"
        )


def add_expense(manager):
    print("\n--- Add New Expense ---")
    title = input("Expense title: ")
    amount = input("Amount (INR): ")
    category = input("Category: ")
    expense_date = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
    try:
        expense = manager.add_expense(title, amount, category, expense_date or None)
        print(f"\nExpense added successfully. Reference ID: {expense['id']}")
    except ValueError as error:
        print(f"\nInput error: {error}")


def show_summary(manager):
    summary = manager.get_summary()
    print("\n--- Expense Summary ---")
    print(f"Number of expenses : {summary['count']}")
    print(f"All-time spending  : ₹{summary['total']:.2f}")
    print(f"This month's total : ₹{summary['monthly_total']:.2f}")
    print("\nCategory-wise spending:")
    if not summary["by_category"]:
        print("No category data available.")
    else:
        for category, amount in summary["by_category"].items():
            print(f"  {category:<18} ₹{amount:.2f}")


def main():
    manager = ExpenseManager()
    while True:
        print("\n" + "=" * 42)
        print("       PERSONAL EXPENSE TRACKER")
        print("=" * 42)
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Delete an expense")
        print("4. View spending summary")
        print("5. Export expenses to CSV")
        print("6. Exit")

        choice = input("\nChoose an option (1-6): ").strip()

        if choice == "1":
            add_expense(manager)
        elif choice == "2":
            show_expenses(manager)
        elif choice == "3":
            show_expenses(manager)
            expense_id = input("\nEnter the expense ID to delete: ").strip()
            removed = manager.delete_expense(expense_id)
            print("Expense deleted." if removed else "No expense found with that ID.")
        elif choice == "4":
            show_summary(manager)
        elif choice == "5":
            try:
                path = manager.export_csv()
                print(f"\nCSV file exported successfully: {path.resolve()}")
            except OSError as error:
                print(f"\nCould not export CSV: {error}")
        elif choice == "6":
            print("\nThank you for using Personal Expense Tracker. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
