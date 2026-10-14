from fastapi import APIRouter, HTTPException, status
from app.db import query_all, query_one
from app.models import AccountsListResponse, AccountItem, TransactionsListResponse, TransactionItem

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=AccountsListResponse)
def list_accounts():
    """Retrieve all active customer accounts with available and ledger balances."""
    rows = query_all("SELECT * FROM accounts ORDER BY created_at ASC")
    accounts = [
        AccountItem(
            id=r["id"],
            account_number=r["account_number"],
            account_name=r["account_name"],
            account_type=r["account_type"],
            currency=r["currency"],
            available_balance=float(r["available_balance"]),
            ledger_balance=float(r["ledger_balance"]),
            status=r["status"]
        )
        for r in rows
    ]
    return AccountsListResponse(accounts=accounts)


@router.get("/{account_id}", response_model=AccountItem)
def get_account_detail(account_id: str):
    """Retrieve single account details by ID."""
    row = query_one("SELECT * FROM accounts WHERE id = ?", (account_id,))
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account '{account_id}' not found"
        )
    return AccountItem(
        id=row["id"],
        account_number=row["account_number"],
        account_name=row["account_name"],
        account_type=row["account_type"],
        currency=row["currency"],
        available_balance=float(row["available_balance"]),
        ledger_balance=float(row["ledger_balance"]),
        status=row["status"]
    )


@router.get("/{account_id}/transactions", response_model=TransactionsListResponse)
def get_account_transactions(account_id: str):
    """Retrieve transaction history for a specific account."""
    acc = query_one("SELECT id FROM accounts WHERE id = ?", (account_id,))
    if not acc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account '{account_id}' not found"
        )

    rows = query_all(
        "SELECT * FROM transactions WHERE account_id = ? ORDER BY date DESC, created_at DESC",
        (account_id,)
    )
    transactions = [
        TransactionItem(
            id=r["id"],
            account_id=r["account_id"],
            date=r["date"],
            description=r["description"],
            type=r["type"],
            amount=float(r["amount"]),
            running_balance=float(r["running_balance"]),
            status=r["status"]
        )
        for r in rows
    ]
    return TransactionsListResponse(account_id=account_id, transactions=transactions)


@router.get("/{account_id}/statement")
def get_statement_summary(account_id: str):
    """Export or retrieve statement metadata for an account."""
    acc = query_one("SELECT * FROM accounts WHERE id = ?", (account_id,))
    if not acc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    txs = query_all("SELECT * FROM transactions WHERE account_id = ? ORDER BY date DESC", (account_id,))
    return {
        "statement_period": "October 2026",
        "account_id": account_id,
        "account_number": acc["account_number"],
        "account_name": acc["account_name"],
        "closing_balance": float(acc["available_balance"]),
        "total_transactions": len(txs),
        "status": "GENERATED"
    }
