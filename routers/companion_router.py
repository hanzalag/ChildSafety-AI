from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import UserSession, CompanionAudit
from services.audit_service import AuditService
from sqlalchemy.future import select

router = APIRouter(prefix="/api/companion", tags=["SafeCompanion Guard"])

class CompanionAuditRequest(BaseModel):
    session_uuid: str = Field(..., description="Active user session identifier")
    companion_prompt: str = Field(..., min_length=1, max_length=2000, description="Prompt sent to AI companion")
    companion_response: str = Field(..., min_length=1, max_length=4000, description="Raw response from AI companion")

class CompanionAuditResponse(BaseModel):
    safety_rating: str
    boundary_violation_detected: bool
    audit_notes: str
    safe_response: str
    audit_id: int

@router.post("/audit", response_model=CompanionAuditResponse)
async def audit_companion(payload: CompanionAuditRequest, db: AsyncSession = Depends(get_db)):
    # Verify or create user session
    result = await db.execute(select(UserSession).filter_by(session_uuid=payload.session_uuid))
    user_session = result.scalars().first()
    
    if not user_session:
        user_session = UserSession(session_uuid=payload.session_uuid, role_type="child")
        db.add(user_session)
        await db.commit()
        await db.refresh(user_session)

    # Perform AI audit
    audit_result = await AuditService.audit_companion_interaction(payload.companion_prompt, payload.companion_response)

    # Log audit to database
    audit_entry = CompanionAudit(
        user_id=user_session.id,
        companion_prompt=payload.companion_prompt,
        companion_response=payload.companion_response,
        safety_rating=audit_result.get("safety_rating", "Safe"),
        boundary_violation_detected=audit_result.get("boundary_violation_detected", False),
        audit_notes=audit_result.get("audit_notes", "")
    )
    db.add(audit_entry)
    await db.commit()
    await db.refresh(audit_entry)

    return {
        "safety_rating": audit_result.get("safety_rating", "Safe"),
        "boundary_violation_detected": audit_result.get("boundary_violation_detected", False),
        "audit_notes": audit_result.get("audit_notes", ""),
        "safe_response": audit_result.get("safe_response", payload.companion_response),
        "audit_id": audit_entry.id
    }