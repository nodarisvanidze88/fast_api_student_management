import sys
from pathlib import Path
from sqlalchemy.sql import text
# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base

db:Session = SessionLocal()

try:
    result = db.execute(text("SELECT 1"))
    print("Database connection successful", result.fetchone())
except Exception as e:
    print("Database connection failed", str(e))
finally:
    db.close()