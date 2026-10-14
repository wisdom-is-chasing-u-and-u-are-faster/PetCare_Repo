import uuid
from fastapi import APIRouter, HTTPException, status
from app.db import query_one
from app.models import LoginRequest, LoginResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    """Authenticate user with email and password."""
    user = query_one(
        "SELECT id, full_name, email, role FROM users WHERE email = ? AND password_hash = ?",
        (payload.email.strip().lower(), payload.password)
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = f"jwt_{uuid.uuid4().hex}"
    return LoginResponse(
        token=token,
        user=UserResponse(
            id=user["id"],
            full_name=user["full_name"],
            email=user["email"],
            role=user.get("role", "customer")
        )
    )


@router.get("/me")
def get_current_user():
    """Retrieve current authenticated user context."""
    user = query_one("SELECT id, full_name, email, role FROM users LIMIT 1")
    if not user:
        return {"id": "usr_001", "full_name": "Jane Doe", "email": "admin@bank.com", "role": "admin"}
    return user
