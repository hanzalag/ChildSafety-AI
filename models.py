import datetime
from sqlalchemy import String, Text, DateTime, Integer, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_uuid: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    role_type: Mapped[str] = mapped_column(String(32), default="child")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    moderation_logs: Mapped[list["ModerationLog"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    companion_audits: Mapped[list["CompanionAudit"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    image_audits: Mapped[list["ImageAuditLog"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_sessions.id"))
    input_text: Mapped[str] = mapped_column(Text)
    is_safe: Mapped[bool] = mapped_column(default=True)
    threat_category: Mapped[str] = mapped_column(String(64), nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    ai_feedback: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user: Mapped["UserSession"] = relationship(back_populates="moderation_logs")


class CompanionAudit(Base):
    __tablename__ = "companion_audits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_sessions.id"))
    companion_prompt: Mapped[str] = mapped_column(Text)
    companion_response: Mapped[str] = mapped_column(Text)
    safety_rating: Mapped[str] = mapped_column(String(32))
    boundary_violation_detected: Mapped[bool] = mapped_column(default=False)
    audit_notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user: Mapped["UserSession"] = relationship(back_populates="companion_audits")


class ImageAuditLog(Base):
    __tablename__ = "image_audit_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_sessions.id"))
    image_filename: Mapped[str] = mapped_column(String(255), nullable=True)
    is_ai_generated: Mapped[bool] = mapped_column(default=False)
    is_harmful: Mapped[bool] = mapped_column(default=False)
    threat_category: Mapped[str] = mapped_column(String(64), nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    ai_feedback: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user: Mapped["UserSession"] = relationship(back_populates="image_audits")