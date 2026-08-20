"""
app/auth/roles.py – Role-Based Access Control (RBAC) dependencies.

Defines role constants and FastAPI dependency factories that
enforce role requirements on protected endpoints.

Roles:
  - 'admin'   : Full platform access, user management
  - 'analyst' : Can run predictions, generate reports
  - 'user'    : Basic access, can view own data

Usage:
    @router.delete("/{id}", dependencies=[Depends(require_role("admin"))])
    def delete_something(): ...

    @router.get("/admin-only")
    def admin_view(user: User = Depends(require_admin)):
        ...
"""

from fastapi import Depends, HTTPException, status
from app.auth.dependencies import get_current_user
from app.models.user import User


ROLE_ADMIN = "admin"
ROLE_ANALYST = "analyst"
ROLE_USER = "user"

ALL_ROLES = [ROLE_ADMIN, ROLE_ANALYST, ROLE_USER]


def require_role(*allowed_roles: str):
    """
    Dependency factory — returns a FastAPI dependency that only allows
    users whose role is in allowed_roles.

    Example:
        @router.delete("/users/{id}", dependencies=[Depends(require_role("admin"))])
        def delete_user(id: int): ...
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Access denied. Required role(s): {list(allowed_roles)}. "
                    f"Your role: '{current_user.role}'."
                ),
            )
        return current_user
    return role_checker


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency: allows only admin users."""
    if current_user.role != ROLE_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )
    return current_user


def require_analyst_or_admin(current_user: User = Depends(get_current_user)) -> User:
    """Dependency: allows analyst or admin users."""
    if current_user.role not in (ROLE_ANALYST, ROLE_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analyst or Admin access required.",
        )
    return current_user
