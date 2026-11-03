"""Unit tests for ExpenseManager."""

import tempfile
import unittest
from pathlib import Path

from expense_manager import ExpenseManager


class ExpenseManagerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "expenses.json"
        self.manager = ExpenseManager(self.data_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_persist_expense(self):
        created = self.manager.add_expense("Lunch", 120, "food", "2026-11-03")
        reloaded = ExpenseManager(self.data_file)
        self.assertEqual(created["title"], "Lunch")
        self.assertEqual(reloaded.get_summary()["total"], 120.0)
        self.assertEqual(reloaded.get_summary()["by_category"]["Food"], 120.0)

    def test_reject_non_positive_amount(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense("Bus", 0, "Travel")

    def test_reject_invalid_date(self):
        with self.assertRaises(ValueError):
            self.manager.add_expense("Book", 250, "Education", "03-11-2026")

    def test_delete_expense(self):
        created = self.manager.add_expense("Tea", 20, "Food", "2026-11-03")
        removed = self.manager.delete_expense(created["id"])
        self.assertIsNotNone(removed)
        self.assertEqual(self.manager.get_summary()["count"], 0)

    def test_csv_export(self):
        self.manager.add_expense("Notebook", 60, "Education", "2026-11-03")
        output = Path(self.temp_dir.name) / "export.csv"
        self.manager.export_csv(output)
        self.assertTrue(output.exists())
        self.assertIn("Notebook", output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
