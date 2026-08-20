"""
app/api/projects.py – Project Management API endpoints.

All endpoints require authentication (JWT Bearer token).

Endpoints:
  GET    /projects         → List current user's projects
  POST   /projects         → Create a new project
  GET    /projects/{id}    → Get a single project by ID
  PUT    /projects/{id}    → Update a project (owner or admin)
  DELETE /projects/{id}    → Delete a project (owner or admin)

"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse
from app.auth.dependencies import get_current_user
from app.auth.roles import require_admin
from app.models.user import User

router = APIRouter()


@router.get(
    "",
    response_model=List[ProjectResponse],
    summary="List my projects",
    description="Returns all projects owned by the currently authenticated user.",
    tags=["Projects"],
)
def get_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns all projects for the authenticated user."""
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    return projects


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    tags=["Projects"],
)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Creates a new solar/wind deployment project owned by the authenticated user.
    All required fields are validated by Pydantic before insertion.
    """
    new_project = Project(
        user_id=current_user.id,
        project_name=payload.project_name,
        description=payload.description,
        state=payload.state,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get a project by ID",
    tags=["Projects"],
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve a single project. Returns 403 if project belongs to another user
    (unless caller is admin).
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Only the owner or an admin can view the project
    if project.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view this project")

    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project",
    tags=["Projects"],
)
def update_project(
    project_id: int,
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing project. Only the owner or an admin can edit.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to update this project")

    project.project_name = payload.project_name
    project.description = payload.description
    project.state = payload.state
    project.latitude = payload.latitude
    project.longitude = payload.longitude

    db.commit()
    db.refresh(project)

    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    tags=["Projects"],
)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a project. Only the owner or an admin can delete.
    Returns 204 No Content on success.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to delete this project")

    db.delete(project)
    db.commit()
