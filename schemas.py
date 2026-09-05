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

class PostCreate(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: Optional[str] = None
    cover_image: Optional[str] = None
    status: Optional[str] = "draft"

class PostOut(PostCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    name: str
    email: str
    subject: Optional[str] = None
    message: str

class MessageOut(MessageCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class VisitCreate(BaseModel):
    path: str
    session_id: str

class HeartbeatCreate(BaseModel):
    session_id: str

class AnalyticsSummary(BaseModel):
    total_visits: int
    unique_visitors: int
    online_now: int
    top_pages: list[dict]
    total_messages: int
