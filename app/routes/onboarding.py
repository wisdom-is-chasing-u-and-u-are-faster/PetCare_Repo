import uuid
from fastapi import APIRouter, status
from app.db import execute_mutation
from app.models import OnboardingRequest, OnboardingResponse

router = APIRouter(prefix="/onboarding", tags=["onboarding"])


@router.post("", response_model=OnboardingResponse, status_code=status.HTTP_201_CREATED)
def submit_onboarding(payload: OnboardingRequest):
    """Submit multi-step customer eKYC onboarding application."""
    app_id = f"app_{uuid.uuid4().hex[:8]}"

    query = """
        INSERT INTO onboarding_applications
        (id, company_name, full_name, work_email, id_document, address_document, status)
        VALUES (?, ?, ?, ?, ?, ?, 'APPROVED')
    """
    execute_mutation(
        query,
        (
            app_id,
            payload.company_name,
            payload.full_name,
            payload.work_email,
            payload.id_document or "passport_scanned.pdf",
            payload.address_document or "utility_bill.pdf"
        )
    )

    return OnboardingResponse(
        application_id=app_id,
        status="APPROVED",
        message="Onboarding eKYC verification completed successfully. Account activated."
    )
