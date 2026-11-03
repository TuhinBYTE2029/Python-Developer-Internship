# Personal Expense Tracker (Task 3)

A Python command-line application for recording, reviewing, summarizing, deleting, and exporting personal expenses.

## Features
- Add expenses with title, amount, category, and date.
- Validate amounts and dates before saving.
- View all expenses, newest first.
- Delete an expense using its reference ID.
- Calculate all-time and current-month spending.
- Display category-wise totals.
- Export records to CSV.
- Persist data locally in `expenses.json`.

## Requirements
- Python 3.10 or later (tested with Python 3.14).
- No third-party packages are required; the application uses Python's standard library.

## Run the application
Open this folder in VS Code and run:

```powershell
python main.py
```

The first run creates `expenses.json` when an expense is added.

## Run tests
From this folder, run:

```powershell
python -m unittest discover -s tests -v
```

## Project structure
```text
task3_expense_tracker/
├── main.py
├── expense_manager.py
├── README.md
└── tests/
    └── test_expense_manager.py
```

## Data format
Expense records are stored locally in JSON. Each record includes a unique reference ID, title, amount, category, and date. CSV export creates `expenses_export.csv`.

## Limitations
This is a local, single-user learning project. It does not connect to a bank account or provide financial advice. Keep personal financial data private.
