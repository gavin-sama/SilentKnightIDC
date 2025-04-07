from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Setup
DATABASE_URL = "sqlite:///./SilentKnight.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# SQLAlchemy model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

app = FastAPI()

# Pydantic model
class UserCreate(BaseModel):
    username: str
    password: str

# Endpoints
@app.get("/users")
def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

@app.post("/users")
def create_user(user: UserCreate):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user
