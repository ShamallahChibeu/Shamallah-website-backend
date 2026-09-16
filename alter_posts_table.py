import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE posts ADD COLUMN IF NOT EXISTS file_url VARCHAR"))
    conn.commit()

print("Done: file_url column added to posts table.")
