from sqlalchemy import Column, String, DateTime, Text, Integer, Boolean, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(LargeBinary, nullable=False)
    display_name = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # GDPR/CCPA
    consent_marketing = Column(Boolean, default=False)
    consent_analytics = Column(Boolean, default=False)
    
    # Relations
    sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("chat_sessions.id"), nullable=False, index=True)
    role = Column(String, nullable=False)  # "user", "assistant", "tool"
    content = Column(Text, nullable=False)
    tool_outputs = Column(Text, nullable=True)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relations
    session = relationship("ChatSession", back_populates="messages")


class Place(Base):
    __tablename__ = "places"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    image_urls = Column(Text, nullable=True)  # JSON array of image URLs
    sources = Column(Text, nullable=True)  # JSON array of source URLs
    created_at = Column(DateTime, default=datetime.utcnow)
    cached_at = Column(DateTime, default=datetime.utcnow)


# Session storage (in-memory for local dev, can be moved to Redis/DB)
_in_memory_sessions = {}
_in_memory_users = {}


def create_in_memory_user(email: str, hashed_password: bytes, display_name: str = None) -> dict:
    """Create user in-memory store (placeholder for DB insert)"""
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": email,
        "hashed_password": hashed_password,
        "display_name": display_name or email.split("@")[0],
        "profile_picture_url": None,
        "created_at": datetime.utcnow(),
        "sessions": [],
    }
    _in_memory_users[email] = user
    return user


def get_in_memory_user(email: str) -> dict:
    """Fetch user from in-memory store"""
    return _in_memory_users.get(email)


def create_in_memory_session(user_id: str, title: str = None) -> dict:
    """Create session in-memory store (placeholder for DB insert)"""
    session_id = str(uuid.uuid4())
    session = {
        "id": session_id,
        "user_id": user_id,
        "title": title,
        "created_at": datetime.utcnow(),
        "messages": [],
    }
    _in_memory_sessions[session_id] = session
    return session


def get_in_memory_session(session_id: str) -> dict:
    """Fetch session from in-memory store"""
    return _in_memory_sessions.get(session_id)


def add_message_to_session(session_id: str, role: str, content: str):
    """Add message to in-memory session"""
    if session_id not in _in_memory_sessions:
        return None
    msg = {
        "role": role,
        "content": content,
        "created_at": datetime.utcnow(),
    }
    _in_memory_sessions[session_id]["messages"].append(msg)
    return msg


def cleanup_old_sessions(retention_days: int = 30):
    """Delete sessions older than retention_days (run as background job)"""
    cutoff = datetime.utcnow() - timedelta(days=retention_days)
    to_delete = [sid for sid, sess in _in_memory_sessions.items() if sess["created_at"] < cutoff]
    for sid in to_delete:
        del _in_memory_sessions[sid]
    return len(to_delete)
