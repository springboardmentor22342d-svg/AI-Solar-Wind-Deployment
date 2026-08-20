from app.database.database import engine
from sqlalchemy import text

tables = ["users", "projects", "solar_predictions", "wind_predictions", "site_analyses", "reports"]

with engine.connect() as conn:
    for table in tables:
        result = conn.execute(text(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table}' ORDER BY ordinal_position"))
        print(f"\n--- {table} ---")
        for row in result.fetchall():
            print(f"  {row[0]:35s} {row[1]}")
