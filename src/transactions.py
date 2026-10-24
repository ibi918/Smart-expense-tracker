from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Optional

from sqlalchemy import select
from src.database import SessionLocal
from src.models import Transaction


def validate_transaction(
    amount, transaction_type: str, category: str, transaction_date: date,
    description: str = ""
) -> tuple[Decimal, str, str, date, str]:
    """Validate and normalize user-provided transaction fields."""
    try:
        normalized_amount = Decimal(str(amount)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise ValueError("Amount must be a valid number.") from exc

    if not normalized_amount.is_finite() or normalized_amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if transaction_type not in {"income", "expense"}:
        raise ValueError("Transaction type must be income or expense.")

    normalized_category = str(category).strip()
    if not normalized_category:
        raise ValueError("Category cannot be empty.")
    if len(normalized_category) > 50:
        raise ValueError("Category must be 50 characters or fewer.")

    normalized_description = str(description or "").strip()
    if len(normalized_description) > 250:
        raise ValueError("Description must be 250 characters or fewer.")
    if not isinstance(transaction_date, date):
        raise ValueError("A valid transaction date is required.")

    return (
        normalized_amount, transaction_type, normalized_category,
        transaction_date, normalized_description
    )


def add_transaction(
    amount, transaction_type: str, category: str, transaction_date: date,
    description: str = ""
) -> Transaction:
    fields = validate_transaction(
        amount, transaction_type, category, transaction_date, description
    )
    amount_value, type_value, category_value, date_value, description_value = fields
    with SessionLocal() as session:
        transaction = Transaction(
            amount=amount_value,
            transaction_type=type_value,
            category=category_value,
            date=date_value,
            description=description_value,
        )
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        # Return a detached object with attributes available after session close.
        return transaction


def get_transactions(
    transaction_type: Optional[str] = None,
    category: Optional[str] = None,
) -> list[Transaction]:
    with SessionLocal() as session:
        statement = select(Transaction).order_by(
            Transaction.date.desc(), Transaction.id.desc()
        )
        if transaction_type in {"income", "expense"}:
            statement = statement.where(Transaction.transaction_type == transaction_type)
        if category:
            statement = statement.where(Transaction.category == category)
        return list(session.scalars(statement).all())


def get_transaction(transaction_id: int) -> Optional[Transaction]:
    with SessionLocal() as session:
        return session.get(Transaction, transaction_id)


def update_transaction(
    transaction_id: int, amount, transaction_type: str, category: str,
    transaction_date: date, description: str = ""
) -> Transaction:
    fields = validate_transaction(
        amount, transaction_type, category, transaction_date, description
    )
    with SessionLocal() as session:
        transaction = session.get(Transaction, transaction_id)
        if transaction is None:
            raise ValueError(f"Transaction {transaction_id} was not found.")
        (
            transaction.amount, transaction.transaction_type, transaction.category,
            transaction.date, transaction.description
        ) = fields
        session.commit()
        session.refresh(transaction)
        return transaction


def delete_transaction(transaction_id: int) -> bool:
    with SessionLocal() as session:
        transaction = session.get(Transaction, transaction_id)
        if transaction is None:
            return False
        session.delete(transaction)
        session.commit()
        return True
