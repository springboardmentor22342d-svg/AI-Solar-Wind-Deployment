"""
app/models/project.py – SQLAlchemy ORM model for the Projects table.
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class Project(Base):
    """
    ORM model mapped to the 'projects' table in PostgreSQL.

    Each project is owned by a user (user_id FK). A user can have many
    projects (1:N relationship). Projects store the geographic location
    and description of a solar/wind deployment site.
    """

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ondelete="CASCADE": if the user is deleted, their projects are too
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    project_name = Column(String(255), nullable=False, index=True)
    description  = Column(Text, nullable=True)
    state        = Column(String(100), nullable=False)

    latitude  = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="projects")

    def __repr__(self) -> str:
        return f"<Project id={self.id} name={self.project_name} owner={self.user_id}>"
