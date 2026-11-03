"""Additional quality-assurance tests for Task 4.

Run from the project folder:
    python -m unittest discover -s tests -v
"""

import csv
import tempfile
import unittest
from pathlib import Path

from expense_manager import ExpenseManager


class ExpenseManagerQualityTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "expenses.json"
        self.manager = ExpenseManager(self.data_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_reject_empty_title(self):
        with self.assertRaisesRegex(ValueError, "title cannot be empty"):
            self.manager.add_expense("   ", 50, "Food")

    def test_reject_empty_category(self):
        with self.assertRaisesRegex(ValueError, "Category cannot be empty"):
            self.manager.add_expense("Lunch", 50, "   ")

    def test_reject_non_numeric_amount(self):
        with self.assertRaisesRegex(ValueError, "valid number"):
            self.manager.add_expense("Lunch", "abc", "Food")

    def test_reject_negative_amount(self):
        with self.assertRaisesRegex(ValueError, "greater than zero"):
            self.manager.add_expense("Lunch", -10, "Food")

    def test_reject_invalid_calendar_date(self):
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            self.manager.add_expense("Lunch", 50, "Food", "2026-02-30")

    def test_missing_expense_file_starts_empty(self):
        self.assertEqual(self.manager.list_expenses(), [])
        self.assertEqual(self.manager.get_summary()["count"], 0)

    def test_delete_unknown_id_does_not_change_records(self):
        self.manager.add_expense("Lunch", 100, "Food", "2026-11-03")
        result = self.manager.delete_expense("unknown-id")
        self.assertIsNone(result)
        self.assertEqual(self.manager.get_summary()["count"], 1)

    def test_expenses_are_persisted_after_reload(self):
        self.manager.add_expense("Lunch", 100, "Food", "2026-11-03")
        reloaded = ExpenseManager(self.data_file)
        self.assertEqual(reloaded.get_summary()["total"], 100.0)
        self.assertEqual(reloaded.get_summary()["count"], 1)

    def test_list_expenses_is_sorted_newest_first(self):
        self.manager.add_expense("Older", 20, "Food", "2026-11-01")
        self.manager.add_expense("Newer", 30, "Food", "2026-11-03")
        titles = [item["title"] for item in self.manager.list_expenses()]
        self.assertEqual(titles, ["Newer", "Older"])

    def test_summary_calculates_category_totals(self):
        self.manager.add_expense("Lunch", 100, "Food", "2026-11-03")
        self.manager.add_expense("Dinner", 200, "food", "2026-11-03")
        self.manager.add_expense("Bus", 40, "Travel", "2026-11-03")
        summary = self.manager.get_summary()
        self.assertEqual(summary["count"], 3)
        self.assertEqual(summary["total"], 340.0)
        self.assertEqual(summary["by_category"]["Food"], 300.0)
        self.assertEqual(summary["by_category"]["Travel"], 40.0)

    def test_csv_export_contains_header_and_expense(self):
        self.manager.add_expense("Notebook", 60, "Education", "2026-11-03")
        output = Path(self.temp_dir.name) / "qa_export.csv"
        self.manager.export_csv(output)
        with output.open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "Notebook")
        self.assertEqual(rows[0]["category"], "Education")

    def test_corrupted_json_reports_read_error(self):
        self.data_file.write_text("{not valid json", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "Could not read expense data"):
            ExpenseManager(self.data_file)


if __name__ == "__main__":
    unittest.main(verbosity=2)
