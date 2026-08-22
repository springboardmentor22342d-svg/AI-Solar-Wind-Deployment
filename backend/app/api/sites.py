from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.site import Site
from app.schemas.site import SiteCreate, SiteResponse
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/sites", response_model=SiteResponse)
def create_site(site: SiteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_site = Site(**site.model_dump())
    db.add(new_site)
    db.commit()
    db.refresh(new_site)
    return new_site

@router.get("/sites", response_model=list[SiteResponse])
def get_sites(db: Session = Depends(get_db)):
    return db.query(Site).all()