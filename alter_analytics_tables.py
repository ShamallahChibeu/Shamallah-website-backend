import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE visits ADD COLUMN IF NOT EXISTS ip_address VARCHAR"))
    conn.execute(text("DROP TABLE IF EXISTS heartbeats"))
    conn.commit()

print("Done: visits.ip_address added, heartbeats table reset for IP-based tracking.")
