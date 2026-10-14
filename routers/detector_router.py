from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import UserSession, ImageAuditLog
from services.gemini_service import GeminiService
from sqlalchemy.future import select

router = APIRouter(prefix="/api/detector", tags=["Media Detective & Computer Vision"])

@router.post("/analyze-image")
async def analyze_image_cv(
    session_uuid: str = Form(...),
    image: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Verify or create user session
    result = await db.execute(select(UserSession).filter_by(session_uuid=session_uuid))
    user_session = result.scalars().first()
    
    if not user_session:
        user_session = UserSession(session_uuid=session_uuid, role_type="child")
        db.add(user_session)
        await db.commit()
        await db.refresh(user_session)

    image_bytes = await image.read()

    system_instruction = (
        "You are AegisYouth AI Advanced Computer Vision & Media Forensic Detective. "
        "Analyze the provided image for synthetic AI generation, deepfake artifacts, inappropriate themes, "
        "violence, grooming indicators, or malicious scams targeting youth. "
        "Return a strictly valid JSON object with keys: "
        "'is_ai_generated' (boolean), "
        "'is_harmful' (boolean), "
        "'threat_category' (string), "
        "'confidence_score' (float between 0.0 and 1.0), "
        "'ai_feedback' (detailed forensic breakdown), "
        "'child_impact_assessment' (impact on child well-being), "
        "'indicators' (list of strings noting visual artifacts or risks), "
        "'educational_guidance' (empowering advice)."
    )

    prompt = "Perform comprehensive computer vision forensics on this uploaded image for child safety and deepfake detection."
    
    analysis = await GeminiService.generate_json_response(prompt, system_instruction, image_bytes=image_bytes)

    # Save to database
    audit_log = ImageAuditLog(
        user_id=user_session.id,
        image_filename=image.filename,
        is_ai_generated=analysis.get("is_ai_generated", False),
        is_harmful=analysis.get("is_harmful", False),
        threat_category=analysis.get("threat_category", "Unknown"),
        confidence_score=analysis.get("confidence_score", 0.9),
        ai_feedback=analysis.get("ai_feedback", "")
    )
    db.add(audit_log)
    await db.commit()
    await db.refresh(audit_log)

    return analysis