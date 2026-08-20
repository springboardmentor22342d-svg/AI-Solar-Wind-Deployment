"""
app/models/user.py – SQLAlchemy ORM model for the Users table.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class User(Base):
    """
    ORM model mapped to the 'users' table in PostgreSQL.

    Relationships:
      - solar_predictions → one user can have many solar predictions (1:N)
      - wind_predictions  → one user can have many wind predictions  (1:N)
      - site_analyses     → one user can have many site analyses     (1:N)
      - reports           → one user can have many reports           (1:N)
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)

    # role: 'admin' | 'analyst' | 'user'
    role = Column(String(50), default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    solar_predictions = relationship("SolarPrediction", back_populates="user", cascade="all, delete-orphan")
    wind_predictions = relationship("WindPrediction", back_populates="user", cascade="all, delete-orphan")
    site_analyses = relationship("SiteAnalysis", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"
