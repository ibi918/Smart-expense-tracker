from decimal import Decimal
import pandas as pd


def transactions_to_dataframe(transactions) -> pd.DataFrame:
    """Convert SQLAlchemy transactions to a clean DataFrame."""
    columns = ["id", "date", "transaction_type", "category", "amount", "description"]
    rows = [
        {
            "id": item.id,
            "date": item.date,
            "transaction_type": item.transaction_type,
            "category": item.category,
            "amount": float(item.amount),
            "description": item.description,
        }
        for item in transactions
    ]
    df = pd.DataFrame(rows, columns=columns)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
    return df


def calculate_summary(transactions) -> dict[str, Decimal]:
    income = sum(
        (Decimal(str(t.amount)) for t in transactions if t.transaction_type == "income"),
        Decimal("0.00"),
    )
    expenses = sum(
        (Decimal(str(t.amount)) for t in transactions if t.transaction_type == "expense"),
        Decimal("0.00"),
    )
    return {
        "income": income,
        "expenses": expenses,
        "balance": income - expenses,
    }


def category_expenses(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["category", "amount"])
    expenses = df[df["transaction_type"] == "expense"]
    return (
        expenses.groupby("category", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )


def monthly_totals(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["month", "income", "expenses"])
    working = df.copy()
    working["month"] = pd.to_datetime(working["date"]).dt.to_period("M").astype(str)
    pivot = working.pivot_table(
        index="month", columns="transaction_type", values="amount",
        aggfunc="sum", fill_value=0
    )
    for column in ("income", "expense"):
        if column not in pivot.columns:
            pivot[column] = 0.0
    result = pivot.rename(columns={"expense": "expenses"}).reset_index()
    return result[["month", "income", "expenses"]].sort_values("month")
