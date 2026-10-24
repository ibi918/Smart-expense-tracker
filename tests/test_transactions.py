from datetime import date
from decimal import Decimal
import pytest

from src.transactions import validate_transaction


def test_valid_transaction_normalizes_values():
    amount, kind, category, tx_date, description = validate_transaction(
        "12.5", "expense", " Food ", date(2026, 1, 1), " Lunch "
    )
    assert amount == Decimal("12.50")
    assert kind == "expense"
    assert category == "Food"
    assert tx_date == date(2026, 1, 1)
    assert description == "Lunch"


@pytest.mark.parametrize("amount", [0, -5, "not-a-number", "NaN", "Infinity"])
def test_invalid_amount_is_rejected(amount):
    with pytest.raises(ValueError):
        validate_transaction(amount, "expense", "Food", date.today())


def test_invalid_type_is_rejected():
    with pytest.raises(ValueError):
        validate_transaction(10, "transfer", "Food", date.today())


def test_empty_category_is_rejected():
    with pytest.raises(ValueError):
        validate_transaction(10, "expense", "  ", date.today())
