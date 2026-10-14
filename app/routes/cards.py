from typing import List
from fastapi import APIRouter, HTTPException, status
from app.db import query_all, query_one, execute_mutation
from app.models import CardItem, CardStatusUpdateRequest, CardLimitsUpdateRequest

router = APIRouter(prefix="/cards", tags=["cards"])


@router.get("", response_model=List[CardItem])
def list_cards():
    """Retrieve all corporate and debit cards."""
    rows = query_all("SELECT * FROM cards ORDER BY created_at ASC")
    return [
        CardItem(
            id=r["id"],
            card_holder=r["card_holder"],
            card_number_masked=r["card_number_masked"],
            card_type=r["card_type"],
            status=r["status"],
            monthly_limit=float(r["monthly_limit"]),
            pos_limit=float(r["pos_limit"]),
            expiry_date=r["expiry_date"]
        )
        for r in rows
    ]


@router.patch("/{card_id}/status")
def toggle_card_status(card_id: str, payload: CardStatusUpdateRequest):
    """Toggle card status (ACTIVE <-> LOCKED)."""
    card = query_one("SELECT * FROM cards WHERE id = ?", (card_id,))
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card '{card_id}' not found"
        )

    new_status = payload.status.upper()
    if new_status not in ["ACTIVE", "LOCKED"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be either 'ACTIVE' or 'LOCKED'"
        )

    execute_mutation("UPDATE cards SET status = ? WHERE id = ?", (new_status, card_id))
    return {
        "id": card_id,
        "status": new_status,
        "message": f"Card is now {new_status}"
    }


@router.patch("/{card_id}/limits")
def update_card_limits(card_id: str, payload: CardLimitsUpdateRequest):
    """Update card monthly and POS spending limits."""
    card = query_one("SELECT * FROM cards WHERE id = ?", (card_id,))
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card '{card_id}' not found"
        )

    execute_mutation(
        "UPDATE cards SET monthly_limit = ?, pos_limit = ? WHERE id = ?",
        (payload.monthly_limit, payload.pos_limit, card_id)
    )
    return {
        "id": card_id,
        "monthly_limit": payload.monthly_limit,
        "pos_limit": payload.pos_limit,
        "message": "Card spending limits updated successfully"
    }
