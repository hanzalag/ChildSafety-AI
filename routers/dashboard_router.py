from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import UserSession, ModerationLog, CompanionAudit
from sqlalchemy.future import select
from sqlalchemy import func

router = APIRouter(prefix="/api/dashboard", tags=["Parent & Educator Dashboard"])

@router.get("/metrics")
async def get_dashboard_metrics(session_uuid: str = Query(..., description="User session identifier"), db: AsyncSession = Depends(get_db)):
    # Find session
    result = await db.execute(select(UserSession).filter_by(session_uuid=session_uuid))
    user_session = result.scalars().first()
    
    if not user_session:
        # Return default zeroed metrics if session doesn't exist yet
        return {
            "total_messages_scanned": 0,
            "safe_messages_count": 0,
            "threats_mitigated": 0,
            "companion_audits_count": 0,
            "safety_score_percentage": 100.0,
            "recent_moderations": [],
            "recent_audits": []
        }

    # Fetch counts
    mod_result = await db.execute(select(ModerationLog).filter_by(user_id=user_session.id).order_by(ModerationLog.created_at.desc()).limit(10))
    moderation_logs = mod_result.scalars().all()

    audit_result = await db.execute(select(CompanionAudit).filter_by(user_id=user_session.id).order_by(CompanionAudit.created_at.desc()).limit(10))
    companion_audits = audit_result.scalars().all()

    total_scans_query = await db.execute(select(func.count(ModerationLog.id)).filter_by(user_id=user_session.id))
    total_scans = total_scans_query.scalar() or 0

    threats_query = await db.execute(select(func.count(ModerationLog.id)).filter_by(user_id=user_session.id, is_safe=False))
    threats_count = threats_query.scalar() or 0

    audits_count_query = await db.execute(select(func.count(CompanionAudit.id)).filter_by(user_id=user_session.id))
    audits_count = audits_count_query.scalar() or 0

    safe_count = total_scans - threats_count
    safety_percentage = (safe_count / total_scans * 100.0) if total_scans > 0 else 100.0

    return {
        "total_messages_scanned": total_scans,
        "safe_messages_count": safe_count,
        "threats_mitigated": threats_count,
        "companion_audits_count": audits_count,
        "safety_score_percentage": round(safety_percentage, 1),
        "recent_moderations": [
            {
                "id": m.id,
                "input_text": m.input_text[:60] + "..." if len(m.input_text) > 60 else m.input_text,
                "is_safe": m.is_safe,
                "threat_category": m.threat_category,
                "created_at": m.created_at.isoformat()
            } for m in moderation_logs
        ],
        "recent_audits": [
            {
                "id": a.id,
                "prompt": a.companion_prompt[:60] + "..." if len(a.companion_prompt) > 60 else a.companion_prompt,
                "safety_rating": a.safety_rating,
                "boundary_violation": a.boundary_violation_detected,
                "created_at": a.created_at.isoformat()
            } for a in companion_audits
        ]
    }