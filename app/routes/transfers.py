import datetime
import uuid
from fastapi import APIRouter, HTTPException, status
from app.db import query_all, query_one, execute_mutation
from app.models import TransferRequest, TransferResponse

router = APIRouter(prefix="/transfers", tags=["transfers"])


@router.get("")
def list_transfers():
    """List recent and pending fund transfers."""
    rows = query_all("SELECT * FROM transfers ORDER BY created_at DESC")
    return {"transfers": [dict(r) for r in rows]}


@router.post("", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def initiate_transfer(payload: TransferRequest):
    """Initiate a domestic fund transfer (Internal, ACH, Wire, RTP) with idempotency."""
    # Check idempotency key if provided
    if payload.idempotency_key:
        existing = query_one(
            "SELECT * FROM transfers WHERE idempotency_key = ?",
            (payload.idempotency_key,)
        )
        if existing:
            return TransferResponse(
                transfer_id=existing["id"],
                reference_number=existing["reference_number"],
                status=existing["status"],
                amount=float(existing["amount"]),
                created_at=str(existing["created_at"])
            )

    # Validate source account
    source = query_one("SELECT * FROM accounts WHERE id = ?", (payload.from_account_id,))
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Source account '{payload.from_account_id}' not found"
        )

    avail_bal = float(source["available_balance"])
    if avail_bal < payload.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient funds. Available: ${avail_bal:,.2f}, Requested: ${payload.amount:,.2f}"
        )

    # Validate or find target account
    target = query_one("SELECT * FROM accounts WHERE id = ?", (payload.to_account_id,))

    transfer_id = f"tr_{uuid.uuid4().hex[:10]}"
    ref_no = f"TRF-{datetime.datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    now_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Update source account balance
    new_src_balance = avail_bal - payload.amount
    execute_mutation(
        "UPDATE accounts SET available_balance = ?, ledger_balance = ? WHERE id = ?",
        (new_src_balance, new_src_balance, payload.from_account_id)
    )

    # Add transaction to source account
    execute_mutation(
        """INSERT INTO transactions (id, account_id, date, description, type, amount, running_balance, status)
           VALUES (?, ?, ?, ?, 'DEBIT', ?, ?, 'COMPLETED')""",
        (
            f"tx_{uuid.uuid4().hex[:8]}",
            payload.from_account_id,
            now_str,
            f"{payload.transfer_type} to {payload.to_account_id} - {payload.memo or 'Transfer'}",
            -payload.amount,
            new_src_balance
        )
    )

    # If internal target account exists, update it too
    if target:
        new_tgt_balance = float(target["available_balance"]) + payload.amount
        execute_mutation(
            "UPDATE accounts SET available_balance = ?, ledger_balance = ? WHERE id = ?",
            (new_tgt_balance, new_tgt_balance, payload.to_account_id)
        )
        execute_mutation(
            """INSERT INTO transactions (id, account_id, date, description, type, amount, running_balance, status)
               VALUES (?, ?, ?, ?, 'CREDIT', ?, ?, 'COMPLETED')""",
            (
                f"tx_{uuid.uuid4().hex[:8]}",
                payload.to_account_id,
                now_str,
                f"{payload.transfer_type} from {payload.from_account_id} - {payload.memo or 'Transfer'}",
                payload.amount,
                new_tgt_balance
            )
        )

    # Record transfer
    insert_sql = """
        INSERT INTO transfers
        (id, reference_number, user_id, from_account_id, to_account_id,
         amount, transfer_type, memo, idempotency_key, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    execute_mutation(
        insert_sql,
        (
            transfer_id,
            ref_no,
            source.get("user_id", "usr_001"),
            payload.from_account_id,
            payload.to_account_id,
            payload.amount,
            payload.transfer_type,
            payload.memo or "",
            payload.idempotency_key or f"idem_{transfer_id}",
            "COMPLETED",
            now_str
        )
    )

    return TransferResponse(
        transfer_id=transfer_id,
        reference_number=ref_no,
        status="COMPLETED",
        amount=payload.amount,
        created_at=now_str
    )
