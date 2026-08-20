from app.database.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name='users' ORDER BY ordinal_position")
    )
    print("Current users table columns:")
    for row in result.fetchall():
        print(f"  {row[0]:35s} {row[1]}")
