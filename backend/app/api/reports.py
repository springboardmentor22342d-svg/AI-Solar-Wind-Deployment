"""
app/api/reports.py – Report Generation endpoints.

All endpoints require authentication (JWT Bearer token).

"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import ReportRequest, ReportResponse
from app.auth.dependencies import get_current_user
from app.auth.roles import require_analyst_or_admin
from app.models.user import User

router = APIRouter()


@router.post("/generate", response_model=ReportResponse, status_code=202)
def request_report_generation(
    request: ReportRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
):
    """
    [ANALYST / ADMIN] Request the generation of a PDF/Excel report.
    Because generation can be slow, this returns 202 Accepted and processes in background.

    TODO (Milestone 2): Save report request to DB with status='generating',
                        add actual generation function to background_tasks.
    """
    raise HTTPException(status_code=501, detail="Report generation not yet implemented. Coming in Milestone 2.")


@router.get("/", response_model=List[ReportResponse])
def get_user_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    [AUTHENTICATED] Get the current user's generated reports.

    TODO (Milestone 2): Fetch reports for current_user from DB.
    """
    raise HTTPException(status_code=501, detail="Report listing not yet implemented. Coming in Milestone 2.")


@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    [AUTHENTICATED] Download a specific generated report file.

    TODO (Milestone 2): Check report exists, verify user owns it, return FileResponse.
    """
    raise HTTPException(status_code=501, detail="Report download not yet implemented. Coming in Milestone 2.")
