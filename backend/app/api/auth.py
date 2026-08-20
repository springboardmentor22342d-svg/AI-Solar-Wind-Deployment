"""
app/api/auth.py – Authentication and User endpoints.

Endpoints:
  POST /api/v1/auth/register  → Register a new user
  POST /api/v1/auth/login     → Login and receive JWT token
  GET  /api/v1/auth/me        → Get current user profile
  GET  /api/v1/auth/users     → List all users (admin only)

Day 5 & 6 – Infosys Virtual Internship
"""

from datetime import timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate, UserLogin, UserResponse
from app.models import User
from app.auth.security import get_password_hash, verify_password, create_access_token
from app.auth.dependencies import get_current_user
from app.auth.roles import require_admin, ROLE_USER
from app.config import settings

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user. Role defaults to 'user'."""
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    # Hash password and create user object
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=hashed_password,
        role=ROLE_USER,  # always defaults to 'user' on self-registration
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login")
def login_user(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Authenticate a user and return a JWT token."""
    # 1. Fetch user by email
    user = db.query(User).filter(User.email == form_data.username).first()

    # 2. Verify existence and password
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Contact an administrator.",
        )

    # 3. Create JWT Token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
    }


@router.get("/me", response_model=UserResponse)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Get the currently authenticated user profile.
    Requires a valid JWT Bearer token in the Authorization header.
    """
    return current_user


@router.get("/users", response_model=List[UserResponse])
def list_all_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    [ADMIN ONLY] List all registered users.
    Returns HTTP 403 if the caller is not an admin.
    """
    users = db.query(User).all()
    return users


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role: str,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    """
    [ADMIN ONLY] Update a user's role.
    Valid roles: 'admin', 'analyst', 'user'
    """
    valid_roles = {"admin", "analyst", "user"}
    if role not in valid_roles:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid role '{role}'. Must be one of: {valid_roles}",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = role
    db.commit()
    db.refresh(user)
    return {"message": f"User {user.email} role updated to '{role}'"}
