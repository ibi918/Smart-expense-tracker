from datetime import date
from decimal import Decimal

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analytics import (
    calculate_summary, category_expenses, monthly_totals,
    transactions_to_dataframe,
)
from src.database import init_db
from src.transactions import add_transaction, delete_transaction, get_transactions

st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide",
)
init_db()

st.title("💰 Smart Expense Tracker")
st.caption("Track income and expenses, understand spending patterns, and monitor your balance.")

with st.sidebar:
    st.header("Add a transaction")
    with st.form("add_transaction_form", clear_on_submit=True):
        transaction_type = st.selectbox("Type", ["expense", "income"])
        amount = st.number_input("Amount (PKR)", min_value=0.01, value=100.00, step=100.00)
        category_options = (
            ["Food", "Transport", "Bills", "Shopping", "Health", "Education", "Rent", "Other"]
            if transaction_type == "expense"
            else ["Salary", "Freelance", "Business", "Gift", "Investment", "Other"]
        )
        category = st.selectbox("Category", category_options)
        transaction_date = st.date_input("Date", value=date.today())
        description = st.text_input("Description (optional)", max_chars=250)
        submitted = st.form_submit_button("Save transaction", use_container_width=True)
        if submitted:
            try:
                add_transaction(
                    amount=amount,
                    transaction_type=transaction_type,
                    category=category,
                    transaction_date=transaction_date,
                    description=description,
                )
                st.success("Transaction saved.")
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))

transactions = get_transactions()
summary = calculate_summary(transactions)
df = transactions_to_dataframe(transactions)

col1, col2, col3 = st.columns(3)
col1.metric("Total income", f"PKR {summary['income']:,.2f}")
col2.metric("Total expenses", f"PKR {summary['expenses']:,.2f}")
col3.metric("Net balance", f"PKR {summary['balance']:,.2f}")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Expenses by category")
    category_df = category_expenses(df)
    if category_df.empty:
        st.info("Add an expense to see your category breakdown.")
    else:
        fig = px.pie(
            category_df, names="category", values="amount", hole=0.45,
            title="Where your money goes"
        )
        st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Monthly income vs expenses")
    monthly_df = monthly_totals(df)
    if monthly_df.empty:
        st.info("Add transactions to see monthly trends.")
    else:
        long_df = monthly_df.melt(
            id_vars="month", value_vars=["income", "expenses"],
            var_name="type", value_name="amount"
        )
        fig = px.bar(
            long_df, x="month", y="amount", color="type", barmode="group",
            labels={"month": "Month", "amount": "Amount (PKR)", "type": "Transaction"}
        )
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Transaction history")
if df.empty:
    st.info("No transactions yet. Add your first transaction using the sidebar.")
else:
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        type_filter = st.selectbox("Filter by type", ["all", "income", "expense"])
    with filter_col2:
        category_filter = st.selectbox("Filter by category", ["all"] + sorted(df["category"].unique().tolist()))
    filtered = df.copy()
    if type_filter != "all":
        filtered = filtered[filtered["transaction_type"] == type_filter]
    if category_filter != "all":
        filtered = filtered[filtered["category"] == category_filter]
    display_df = filtered.rename(columns={
        "id": "ID", "date": "Date", "transaction_type": "Type",
        "category": "Category", "amount": "Amount (PKR)", "description": "Description"
    })
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    with st.expander("Delete a transaction"):
        ids = filtered["id"].tolist()
        if not ids:
            st.write("No transactions match the current filters.")
        else:
            chosen_id = st.selectbox("Choose transaction ID", ids)
            if st.button("Delete selected transaction", type="secondary"):
                if delete_transaction(int(chosen_id)):
                    st.success(f"Transaction {chosen_id} deleted.")
                    st.rerun()
                else:
                    st.error("Transaction could not be found.")
