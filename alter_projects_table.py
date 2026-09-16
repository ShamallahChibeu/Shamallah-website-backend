import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS image_url VARCHAR"))
    conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS tags VARCHAR"))
    conn.commit()

print("Done: image_url and tags columns added to projects table.")
