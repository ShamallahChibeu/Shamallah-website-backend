from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models, schemas, crud, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://shamallah-website-frontend.vercel.app", "https://shamallah.dev", "https://www.shamallah.dev"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

@app.get("/")
def read_root():
    return {"message": "Shamallah's website API is running"}

@app.post("/projects", response_model=schemas.ProjectOut)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_project(db, project)

@app.get("/projects", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)

@app.get("/projects/{project_id}", response_model=schemas.ProjectOut)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.put("/projects/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_project = crud.update_project(db, project_id, project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@app.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_project = crud.delete_project(db, project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

@app.post("/posts", response_model=schemas.PostOut)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_post(db, post)

@app.get("/posts", response_model=list[schemas.PostOut])
def list_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)

@app.get("/posts/{post_id}", response_model=schemas.PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.put("/posts/{post_id}", response_model=schemas.PostOut)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_post = crud.update_post(db, post_id, post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_post = crud.delete_post(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}

@app.post("/messages", response_model=schemas.MessageOut)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db, message)

@app.get("/messages", response_model=list[schemas.MessageOut])
def list_messages(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.get_messages(db)

@app.delete("/messages/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_message = crud.delete_message(db, message_id)
    if db_message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted successfully"}

@app.post("/visits")
def create_visit(visit: schemas.VisitCreate, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    crud.create_visit(db, visit.path, ip)
    return {"status": "ok"}

@app.post("/heartbeat")
def heartbeat(request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    crud.upsert_heartbeat(db, ip)
    return {"status": "ok"}

@app.post("/clicks")
def create_click(click: schemas.ClickCreate, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    crud.create_click(db, click.type, ip)
    return {"status": "ok"}

@app.get("/analytics", response_model=schemas.AnalyticsSummary)
def analytics(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.get_analytics_summary(db)

@app.post("/experiences", response_model=schemas.ExperienceOut)
def create_experience(experience: schemas.ExperienceCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.create_experience(db, experience)

@app.get("/experiences", response_model=list[schemas.ExperienceOut])
def list_experiences(db: Session = Depends(get_db)):
    return crud.get_experiences(db)

@app.get("/experiences/{experience_id}", response_model=schemas.ExperienceOut)
def read_experience(experience_id: int, db: Session = Depends(get_db)):
    db_experience = crud.get_experience(db, experience_id)
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return db_experience

@app.put("/experiences/{experience_id}", response_model=schemas.ExperienceOut)
def update_experience(experience_id: int, experience: schemas.ExperienceCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_experience = crud.update_experience(db, experience_id, experience)
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return db_experience

@app.delete("/experiences/{experience_id}")
def delete_experience(experience_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_experience = crud.delete_experience(db, experience_id)
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return {"message": "Experience deleted successfully"}

@app.post("/login", response_model=schemas.Token)
def login(credentials: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
