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

def create_visit(db: Session, visit: schemas.VisitCreate):
    db_visit = models.Visit(path=visit.path, session_id=visit.session_id)
    db.add(db_visit)
    db.commit()
    return db_visit

def upsert_heartbeat(db: Session, session_id: str):
    hb = db.query(models.Heartbeat).filter(models.Heartbeat.session_id == session_id).first()
    if hb:
        hb.last_seen = datetime.utcnow()
    else:
        hb = models.Heartbeat(session_id=session_id, last_seen=datetime.utcnow())
        db.add(hb)
    db.commit()
    return hb

def get_analytics_summary(db: Session):
    total_visits = db.query(models.Visit).count()
    unique_visitors = db.query(models.Visit.session_id).distinct().count()
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
    return {
        "total_visits": total_visits,
        "unique_visitors": unique_visitors,
        "online_now": online_now,
        "top_pages": top_pages,
        "total_messages": total_messages,
    }
