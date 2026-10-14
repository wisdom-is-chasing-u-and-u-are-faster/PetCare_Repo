from fastapi import APIRouter
from app.db import query_all, query_one
from app.models import DashboardSummaryResponse, TransactionItem

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary():
    """Retrieve consolidated dashboard overview KPIs, balances, cards, and recent activity."""
    acc_rows = query_all("SELECT available_balance FROM accounts")
    total_balance = sum(float(r["available_balance"]) for r in acc_rows) if acc_rows else 0.0

    total_accounts = len(acc_rows)

    card_rows = query_all("SELECT id FROM cards WHERE status = 'ACTIVE'")
    active_cards = len(card_rows)

    pending_transfers_count = query_one(
        "SELECT COUNT(*) as count FROM transfers WHERE status = 'PENDING'"
    )
    pending_count = pending_transfers_count["count"] if pending_transfers_count else 0

    recent_tx_rows = query_all(
        "SELECT * FROM transactions ORDER BY date DESC, created_at DESC LIMIT 5"
    )
    recent_transactions = [
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
        for r in recent_tx_rows
    ]

    return DashboardSummaryResponse(
        total_balance=total_balance,
        total_accounts=total_accounts,
        active_cards=active_cards,
        pending_transfers_count=pending_count,
        recent_transactions=recent_transactions
    )
