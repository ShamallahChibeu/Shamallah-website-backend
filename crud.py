from datetime import datetime, timedelta
from sqlalchemy import func as sql_func
from sqlalchemy.orm import Session
import models, schemas

def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects(db: Session):
    return db.query(models.Project).all()

def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def update_project(db: Session, project_id: int, project: schemas.ProjectCreate):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        return None
    for key, value in project.model_dump().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        return None
    db.delete(db_project)
    db.commit()
    return db_project

def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session):
    return db.query(models.Post).all()

def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def update_post(db: Session, post_id: int, post: schemas.PostCreate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        return None
    for key, value in post.model_dump().items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        return None
    db.delete(db_post)
    db.commit()
    return db_post

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(**message.model_dump())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_messages(db: Session):
    return db.query(models.Message).order_by(models.Message.created_at.desc()).all()

def create_visit(db: Session, path: str, ip_address: str):
    db_visit = models.Visit(path=path, ip_address=ip_address)
    db.add(db_visit)
    db.commit()
    return db_visit

def upsert_heartbeat(db: Session, ip_address: str):
    hb = db.query(models.Heartbeat).filter(models.Heartbeat.ip_address == ip_address).first()
    if hb:
        hb.last_seen = datetime.utcnow()
    else:
        hb = models.Heartbeat(ip_address=ip_address, last_seen=datetime.utcnow())
        db.add(hb)
    db.commit()
    return hb

def create_click(db: Session, click_type: str, ip_address: str):
    db_click = models.ClickEvent(type=click_type, ip_address=ip_address)
    db.add(db_click)
    db.commit()
    return db_click

def get_analytics_summary(db: Session):
    total_visits = db.query(models.Visit).count()
    unique_visitors = db.query(models.Visit.ip_address).filter(models.Visit.ip_address.isnot(None)).distinct().count()
    cutoff = datetime.utcnow() - timedelta(minutes=5)
    online_now = db.query(models.Heartbeat).filter(models.Heartbeat.last_seen >= cutoff).count()
    top_pages_query = (
        db.query(models.Visit.path, sql_func.count(models.Visit.id).label("count"))
        .group_by(models.Visit.path)
        .order_by(sql_func.count(models.Visit.id).desc())
        .limit(10)
        .all()
    )
    top_pages = [{"path": p, "count": c} for p, c in top_pages_query]
    total_messages = db.query(models.Message).count()
    total_social_clicks = db.query(models.ClickEvent).count()
    unique_clickers = db.query(models.ClickEvent.ip_address).filter(models.ClickEvent.ip_address.isnot(None)).distinct().count()
    success_rate = round((unique_clickers / unique_visitors) * 100, 1) if unique_visitors > 0 else 0.0
    return {
        "total_visits": total_visits,
        "unique_visitors": unique_visitors,
        "online_now": online_now,
        "top_pages": top_pages,
        "total_messages": total_messages,
        "total_social_clicks": total_social_clicks,
        "success_rate": success_rate,
    }

def create_experience(db: Session, experience: schemas.ExperienceCreate):
    db_experience = models.Experience(**experience.model_dump())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience

def get_experiences(db: Session):
    return db.query(models.Experience).order_by(models.Experience.id.desc()).all()

def get_experience(db: Session, experience_id: int):
    return db.query(models.Experience).filter(models.Experience.id == experience_id).first()

def update_experience(db: Session, experience_id: int, experience: schemas.ExperienceCreate):
    db_experience = db.query(models.Experience).filter(models.Experience.id == experience_id).first()
    if db_experience is None:
        return None
    for key, value in experience.model_dump().items():
        setattr(db_experience, key, value)
    db.commit()
    db.refresh(db_experience)
    return db_experience

def delete_experience(db: Session, experience_id: int):
    db_experience = db.query(models.Experience).filter(models.Experience.id == experience_id).first()
    if db_experience is None:
        return None
    db.delete(db_experience)
    db.commit()
    return db_experience
