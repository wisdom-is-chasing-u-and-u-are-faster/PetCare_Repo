from typing import Optional, List
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    password: str
    remember_me: Optional[bool] = False


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    role: str


class LoginResponse(BaseModel):
    token: str
    user: UserResponse


class OnboardingRequest(BaseModel):
    company_name: str
    full_name: str
    work_email: str
    id_document: Optional[str] = None
    address_document: Optional[str] = None


class OnboardingResponse(BaseModel):
    application_id: str
    status: str
    message: str


class AccountItem(BaseModel):
    id: str
    account_number: str
    account_name: str
    account_type: str
    currency: str
    available_balance: float
    ledger_balance: float
    status: str


class AccountsListResponse(BaseModel):
    accounts: List[AccountItem]


class TransactionItem(BaseModel):
    id: str
    account_id: str
    date: str
    description: str
    type: str
    amount: float
    running_balance: float
    status: str


class TransactionsListResponse(BaseModel):
    account_id: str
    transactions: List[TransactionItem]


class TransferRequest(BaseModel):
    from_account_id: str
    to_account_id: str
    amount: float = Field(..., gt=0)
    transfer_type: str = "Internal Transfer"
    memo: Optional[str] = ""
    idempotency_key: Optional[str] = None


class TransferResponse(BaseModel):
    transfer_id: str
    reference_number: str
    status: str
    amount: float
    created_at: str


class CardItem(BaseModel):
    id: str
    card_holder: str
    card_number_masked: str
    card_type: str
    status: str
    monthly_limit: float
    pos_limit: float
    expiry_date: str


class CardStatusUpdateRequest(BaseModel):
    status: str


class CardLimitsUpdateRequest(BaseModel):
    monthly_limit: float = Field(..., gt=0)
    pos_limit: float = Field(..., gt=0)


class DashboardSummaryResponse(BaseModel):
    total_balance: float
    total_accounts: int
    active_cards: int
    pending_transfers_count: int
    recent_transactions: List[TransactionItem]
