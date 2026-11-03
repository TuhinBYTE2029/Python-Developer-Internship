"""Core logic for the Personal Expense Tracker."""

import csv
import json
from datetime import date, datetime
from pathlib import Path
from uuid import uuid4


class ExpenseManager:
    """Manage expense records stored in a local JSON file."""

    def __init__(self, data_file="expenses.json"):
        self.data_file = Path(data_file)
        self.expenses = self._load_expenses()

    def _load_expenses(self):
        if not self.data_file.exists():
            return []
        try:
            with self.data_file.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("Expense data must be a list.")
            return data
        except (json.JSONDecodeError, OSError) as error:
            raise RuntimeError(f"Could not read expense data: {error}") from error

    def _save_expenses(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump(self.expenses, file, indent=4)

    @staticmethod
    def _validate_date(expense_date):
        try:
            datetime.strptime(expense_date, "%Y-%m-%d")
        except ValueError as error:
            raise ValueError("Date must use YYYY-MM-DD format.") from error

    def add_expense(self, title, amount, category, expense_date=None):
        title = title.strip()
        category = category.strip().title()
        if not title:
            raise ValueError("Expense title cannot be empty.")
        if not category:
            raise ValueError("Category cannot be empty.")

        try:
            amount = float(amount)
        except (TypeError, ValueError) as error:
            raise ValueError("Amount must be a valid number.") from error
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        expense_date = expense_date or date.today().isoformat()
        self._validate_date(expense_date)

        expense = {
            "id": str(uuid4())[:8],
            "title": title,
            "amount": round(amount, 2),
            "category": category,
            "date": expense_date,
        }
        self.expenses.append(expense)
        self._save_expenses()
        return expense

    def list_expenses(self):
        return sorted(self.expenses, key=lambda item: item["date"], reverse=True)

    def delete_expense(self, expense_id):
        for index, expense in enumerate(self.expenses):
            if expense["id"] == expense_id:
                removed = self.expenses.pop(index)
                self._save_expenses()
                return removed
        return None

    def get_summary(self):
        total = sum(item["amount"] for item in self.expenses)
        by_category = {}
        for item in self.expenses:
            by_category[item["category"]] = (
                by_category.get(item["category"], 0) + item["amount"]
            )
        current_month = date.today().strftime("%Y-%m")
        monthly_total = sum(
            item["amount"] for item in self.expenses
            if item["date"].startswith(current_month)
        )
        return {
            "total": round(total, 2),
            "count": len(self.expenses),
            "monthly_total": round(monthly_total, 2),
            "by_category": {
                key: round(value, 2) for key, value in sorted(by_category.items())
            },
        }

    def export_csv(self, output_file="expenses_export.csv"):
        fields = ["id", "title", "amount", "category", "date"]
        output_path = Path(output_file)
        with output_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(self.list_expenses())
        return output_path
