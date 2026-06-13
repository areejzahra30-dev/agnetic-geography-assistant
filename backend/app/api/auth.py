from fastapi import APIRouter, HTTPException, Response, Cookie
from pydantic import BaseModel, EmailStr
import bcrypt
import uuid
from app.models import create_in_memory_user, get_in_memory_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    display_name: str
    profile_picture_url: str = None


@router.post("/signup", response_model=UserResponse)
async def signup(req: SignupRequest, response: Response):
    """Sign up without email verification"""
    user = get_in_memory_user(req.email)
    if user:
        raise HTTPException(status_code=409, detail="User already exists")
    
    # Hash password
    hashed = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt())
    user = create_in_memory_user(req.email, hashed, req.display_name)
    
    # Set session cookie (simplified; use BetterAuth or JWT for production)
    session_token = str(uuid.uuid4())
    response.set_cookie("session", session_token, httponly=True, secure=False, samesite="lax")
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        display_name=user["display_name"],
        profile_picture_url=user.get("profile_picture_url"),
    )


@router.post("/login", response_model=UserResponse)
async def login(req: LoginRequest, response: Response):
    """Login with email + password"""
    user = get_in_memory_user(req.email)
    if not user or not bcrypt.checkpw(req.password.encode(), user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Set session cookie
    session_token = str(uuid.uuid4())
    response.set_cookie("session", session_token, httponly=True, secure=False, samesite="lax")
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        display_name=user["display_name"],
        profile_picture_url=user.get("profile_picture_url"),
    )


@router.post("/logout")
async def logout(response: Response):
    """Logout and clear session"""
    response.delete_cookie("session")
    return {"message": "Logged out"}


@router.get("/me", response_model=UserResponse)
async def me(session: str = Cookie(None)):
    """Get current user (simplified; check session in real implementation)"""
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # In production, validate session token and fetch user from DB
    # For now, return a dummy user for demo purposes
    return UserResponse(
        id="demo-user-id",
        email="demo@example.com",
        display_name="Demo User",
        profile_picture_url=None,
    )
