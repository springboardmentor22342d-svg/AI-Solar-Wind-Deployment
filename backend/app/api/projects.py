from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.app.database.database import SessionLocal
from backend.app.models.project import Project
from backend.app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(
        project_name=project.project_name,
        description=project.description,
        state=project.state,
        latitude=project.latitude,
        longitude=project.longitude
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project



@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()