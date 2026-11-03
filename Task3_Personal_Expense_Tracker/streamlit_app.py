"""Streamlit web interface for the Personal Expense Tracker."""
import csv
import io
from datetime import date

import streamlit as st

from expense_manager import ExpenseManager

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💸",
    layout="wide",
)

st.title("💸 Personal Expense Tracker")
st.caption("Track your spending, review summaries, and export your expenses.")

@st.cache_resource
def get_manager():
    return ExpenseManager("expenses.json")

manager = get_manager()

# Refresh manager data on every rerun so the interface reflects saved changes.
manager.expenses = manager._load_expenses()

summary = manager.get_summary()
col1, col2, col3 = st.columns(3)
col1.metric("Total spending", f"₹{summary['total']:,.2f}")
col2.metric("This month", f"₹{summary['monthly_total']:,.2f}")
col3.metric("Number of expenses", summary["count"])

st.divider()
add_tab, view_tab, summary_tab = st.tabs(
    ["➕ Add expense", "📋 View / delete expenses", "📊 Category summary"]
)

with add_tab:
    st.subheader("Add a new expense")
    with st.form("add_expense_form", clear_on_submit=True):
        title = st.text_input("Expense title", placeholder="e.g. Lunch")
        amount = st.number_input("Amount (₹)", min_value=0.01, step=1.0, format="%.2f")
        category = st.text_input("Category", placeholder="e.g. Food")
        expense_date = st.date_input("Date", value=date.today())
        submitted = st.form_submit_button("Save expense", type="primary")
    if submitted:
        try:
            expense = manager.add_expense(
                title, amount, category, expense_date.isoformat()
            )
            st.success(f"Expense saved successfully. Reference ID: {expense['id']}")
            st.rerun()
        except (ValueError, RuntimeError, OSError) as error:
            st.error(str(error))

with view_tab:
    st.subheader("Your expenses")
    expenses = manager.list_expenses()
    if expenses:
        st.dataframe(
            [
                {
                    "Date": item["date"],
                    "Title": item["title"],
                    "Category": item["category"],
                    "Amount (₹)": f"₹{item['amount']:,.2f}",
                    "Reference ID": item["id"],
                }
                for item in expenses
            ],
            use_container_width=True,
            hide_index=True,
        )
        ids = [item["id"] for item in expenses]
        selected_id = st.selectbox(
            "Select an expense to delete",
            options=ids,
            format_func=lambda value: next(
                f"{item['date']} — {item['title']} — ₹{item['amount']:,.2f} ({item['id']})"
                for item in expenses if item["id"] == value
            ),
        )
        if st.button("Delete selected expense", type="secondary"):
            removed = manager.delete_expense(selected_id)
            if removed:
                st.success(f"Deleted: {removed['title']}")
                st.rerun()
            else:
                st.warning("That expense could not be found.")
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(
            csv_buffer, fieldnames=["id", "title", "amount", "category", "date"]
        )
        writer.writeheader()
        writer.writerows(expenses)
        st.download_button(
            "⬇️ Download expenses as CSV",
            data=csv_buffer.getvalue().encode("utf-8"),
            file_name="expenses_export.csv",
            mime="text/csv",
        )
    else:
        st.info("No expenses yet. Add your first expense in the Add expense tab.")

with summary_tab:
    st.subheader("Spending by category")
    categories = summary["by_category"]
    if categories:
        st.bar_chart(
            [{"Category": category, "Amount (₹)": amount}
             for category, amount in categories.items()],
            x="Category",
            y="Amount (₹)",
        )
        for category, amount in categories.items():
            st.write(f"**{category}:** ₹{amount:,.2f}")
    else:
        st.info("Category summaries will appear after you add expenses.")

st.divider()
st.caption(
    "Learning project: expense data is stored in a local JSON file on the hosting "
    "environment. Avoid entering sensitive financial information."
)
