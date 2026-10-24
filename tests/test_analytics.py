from datetime import date
from decimal import Decimal
from types import SimpleNamespace

from src.analytics import calculate_summary, category_expenses, monthly_totals, transactions_to_dataframe


def sample_transactions():
    return [
        SimpleNamespace(id=1, date=date(2026, 1, 5), transaction_type="income",
                        category="Salary", amount=Decimal("50000.00"), description="Pay"),
        SimpleNamespace(id=2, date=date(2026, 1, 6), transaction_type="expense",
                        category="Food", amount=Decimal("1500.00"), description="Groceries"),
        SimpleNamespace(id=3, date=date(2026, 2, 2), transaction_type="expense",
                        category="Food", amount=Decimal("500.00"), description="Lunch"),
    ]


def test_calculate_summary():
    result = calculate_summary(sample_transactions())
    assert result["income"] == Decimal("50000.00")
    assert result["expenses"] == Decimal("2000.00")
    assert result["balance"] == Decimal("48000.00")


def test_transactions_to_dataframe():
    df = transactions_to_dataframe(sample_transactions())
    assert len(df) == 3
    assert "amount" in df.columns


def test_category_expenses():
    df = transactions_to_dataframe(sample_transactions())
    result = category_expenses(df)
    assert result.iloc[0]["category"] == "Food"
    assert result.iloc[0]["amount"] == 2000


def test_monthly_totals():
    df = transactions_to_dataframe(sample_transactions())
    result = monthly_totals(df)
    assert len(result) == 2
    assert list(result.columns) == ["month", "income", "expenses"]
