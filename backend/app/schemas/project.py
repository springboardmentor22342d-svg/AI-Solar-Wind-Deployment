"""
app/schemas/project.py – Pydantic schemas for Project data validation.

These schemas define what the API accepts (request body) and returns (response body).
Pydantic automatically validates incoming data and returns clear error messages
when validation fails — preventing invalid data from reaching the database.

Validation rules enforced:
  - project_name : required, cannot be empty/whitespace
  - state        : required, cannot be empty/whitespace
  - latitude     : required, must be between -90.0 and 90.0
  - longitude    : required, must be between -180.0 and 180.0
  - description  : optional

"""

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from datetime import datetime


class ProjectCreate(BaseModel):
    """
    Schema for creating a new project (POST /projects request body).

    Pydantic validates every field before it reaches the database:
      - Empty strings are rejected
      - Out-of-range lat/lon values are rejected
      - Missing required fields return a 422 Unprocessable Entity error
    """

    project_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Name of the solar/wind project",
        examples=["Odisha Solar Farm"],
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional description of the project",
        examples=["Large-scale solar installation in eastern India"],
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Indian state where the project is located",
        examples=["Odisha"],
    )
    latitude: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
        description="Geographic latitude of the project site (-90 to 90)",
        examples=[20.9517],
    )
    longitude: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
        description="Geographic longitude of the project site (-180 to 180)",
        examples=[85.0985],
    )

    @field_validator("project_name", "state")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        """Reject strings that are entirely whitespace."""
        if not value.strip():
            raise ValueError("Field cannot be blank or whitespace only")
        return value.strip()


class ProjectResponse(BaseModel):
    """
    Schema for the API response when returning a project.

    model_config = ConfigDict(from_attributes=True) tells Pydantic
    to read data from SQLAlchemy ORM objects (not just plain dicts).
    """

    id: int
    user_id: int
    project_name: str
    description: Optional[str]
    state: str
    latitude: float
    longitude: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
