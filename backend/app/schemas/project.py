from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ProjectCreate(BaseModel):
    project_name: str = Field(..., min_length=1)
    description: Optional[str] = None
    state: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class ProjectResponse(BaseModel):
    id: int
    project_name: str
    description: Optional[str]
    state: Optional[str]
    latitude: float
    longitude: float
    created_at: datetime

    class Config:
        from_attributes = True