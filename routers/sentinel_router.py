from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import UserSession, ModerationLog
from services.moderation_service import ModerationService
from utils.security import generate_session_uuid
from sqlalchemy.future import select

router = APIRouter(prefix="/api/sentinel", tags=["SafeChat Sentinel"])

class MessageAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000, description="Message text to analyze")
    session_uuid: str = Field(..., description="Active user session identifier")

class MessageAnalysisResponse(BaseModel):
    is_safe: bool
    threat_category: str
    confidence_score: float
    ai_feedback: str
    reframed_text: str
    log_id: int

@router.post("/analyze", response_model=MessageAnalysisResponse)
async def analyze_message(payload: MessageAnalysisRequest, db: AsyncSession = Depends(get_db)):
    # Verify or create user session
    result = await db.execute(select(UserSession).filter_by(session_uuid=payload.session_uuid))
    user_session = result.scalars().first()
    
    if not user_session:
        user_session = UserSession(session_uuid=payload.session_uuid, role_type="child")
        db.add(user_session)
        await db.commit()
        await db.refresh(user_session)

    # Perform AI moderation analysis
    analysis = await ModerationService.analyze_message(payload.text)

    # Log interaction to database
    log_entry = ModerationLog(
        user_id=user_session.id,
        input_text=payload.text,
        is_safe=analysis.get("is_safe", True),
        threat_category=analysis.get("threat_category", "None"),
        confidence_score=analysis.get("confidence_score", 1.0),
        ai_feedback=analysis.get("ai_feedback", "")
    )
    db.add(log_entry)
    await db.commit()
    await db.refresh(log_entry)

    return {
        "is_safe": analysis.get("is_safe", True),
        "threat_category": analysis.get("threat_category", "None"),
        "confidence_score": analysis.get("confidence_score", 1.0),
        "ai_feedback": analysis.get("ai_feedback", ""),
        "reframed_text": analysis.get("reframed_text", payload.text),
        "log_id": log_entry.id
    }