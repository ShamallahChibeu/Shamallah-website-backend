from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    content: Optional[str] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    status: Optional[str] = "draft"

class ProjectOut(ProjectCreate):
    id: int
    created_at: datetime

class Config:
        from_attributes = True
class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str