"""
app/schemas/report.py – Pydantic schemas for Report validation.

"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ReportRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    report_type: str = Field(..., description="Must be one of: 'solar', 'wind', 'site_analysis', 'comprehensive'")


class ReportResponse(BaseModel):
    id: int
    user_id: int
    title: str
    report_type: str
    file_path: Optional[str]
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
