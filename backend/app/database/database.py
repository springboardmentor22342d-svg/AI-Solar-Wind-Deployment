"""
app/database/connection.py – Database engine and session factory.

SQLAlchemy 2.0 synchronous engine setup for PostgreSQL.
Uses dependency injection pattern for FastAPI route handlers.

Key SQL Concepts Demonstrated Here:
  - Connection Pooling: SQLAlchemy manages a pool of reusable DB connections
    to avoid the overhead of creating a new connection per request.
  - Session: A unit-of-work that tracks all pending DB changes.
    session.commit() → writes changes to DB
    session.rollback() → undoes changes on error
  - Dependency Injection: get_db() is used as a FastAPI Depends() parameter
    so each route handler gets its own session that auto-closes.

"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# create_engine connects to PostgreSQL using the DATABASE_URL from .env
# pool_pre_ping=True → tests connections before using them (handles DB restarts)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,         # max 10 persistent connections in the pool
    max_overflow=20,      # up to 20 extra connections if pool is full
    echo=settings.DEBUG,  # print SQL statements to console in DEBUG mode
)

# SessionLocal is the factory — calling SessionLocal() creates a new session.
SessionLocal = sessionmaker(
    autocommit=False,   # we commit manually — prevents accidental writes
    autoflush=False,    # we control when pending changes are sent to DB
    bind=engine,
)


# All ORM models (in models/) inherit from Base.
# SQLAlchemy uses Base.metadata to track all table definitions.
class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    Every model that inherits from Base will be mapped to a DB table.
    """
    pass


def get_db():
    """
    FastAPI dependency that provides a database session per request.

    Usage in a route:
        @router.get("/items")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()

    The try/finally block ensures the session is always closed,
    even if an exception occurs during request processing.
    """
    db = SessionLocal()
    try:
        yield db          # provide session to the route handler
        db.commit()       # commit on successful request
    except Exception:
        db.rollback()     # rollback on any error
        raise
    finally:
        db.close()        # always release the connection back to pool


def test_db_connection() -> bool:
    """
    Tests whether the database connection is healthy.
    Called at application startup to fail fast if DB is unavailable.

    Returns:
        True if connection succeeded, False otherwise.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False
