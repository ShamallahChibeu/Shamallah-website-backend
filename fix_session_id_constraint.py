import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE visits ALTER COLUMN session_id DROP NOT NULL"))
    conn.commit()

print("Done: session_id no longer required on visits table.")
