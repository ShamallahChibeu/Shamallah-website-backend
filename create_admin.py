from database import SessionLocal
from models import User
from auth import get_password_hash

db = SessionLocal()

email = input("Enter admin email: ")
password = input("Enter admin password: ")

existing = db.query(User).filter(User.email == email).first()
if existing:
    print("User already exists.")
else:
    new_user = User(email=email, hashed_password=get_password_hash(password))
    db.add(new_user)
    db.commit()
    print(f"Admin user {email} created successfully.")

db.close()