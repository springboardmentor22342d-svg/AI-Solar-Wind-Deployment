"""
app/auth/dependencies.py – FastAPI dependencies for authentication.

"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import User

# This tells FastAPI where the login endpoint is (for swagger UI integration)
# We use standard OAuth2 password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Dependency that decodes the JWT token, extracts the user ID, 
    and fetches the user from the database.
    
    Use this in routes that require authentication:
        @router.get("/protected")
        def protected_route(user: User = Depends(get_current_user)):
            ...
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token using our secret key
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        # Extract the user ID (stored in the 'sub' subject claim)
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
            
        token_data_id = int(user_id_str)
        
    except (JWTError, ValueError):
        raise credentials_exception
        
    # Fetch user from DB
    user = db.query(User).filter(User.id == token_data_id).first()
    
    if user is None:
        raise credentials_exception
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user
