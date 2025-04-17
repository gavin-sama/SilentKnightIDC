from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import json

# Setup
DATABASE_URL = "sqlite:///./SilentKnight.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# SQLAlchemy model
class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender = Column(String, nullable=False)
    receiver = Column(String, nullable=False)
    message = Column(String, nullable=False)

app = FastAPI()

# Pydantic model
class UserCreate(BaseModel):
    username: str
    password: str

class MessageCreate(BaseModel):
    sender: str
    receiver: str
    message: str

# Endpoints
@app.get("/")
def read_root():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

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
    
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.close()

@app.post("/send_message")
def append_message(message_info: MessageCreate):
    db = SessionLocal()

    receiving_user = db.query(User).filter(User.username == message_info.receiver).first().username
    if not receiving_user:
        db.close()
        raise HTTPException(status_code=404, detail="Username not found")

    new_message = Message(**message_info.model_dump())

    db.add(new_message)
    db.commit()
    db.close()

@app.get("/messages/{username}")
def read_all_messages(username: str):
    db = SessionLocal()

    valid_user = db.query(User).filter(User.username == username).first().username
    if valid_user:
        result_messages = db.query(Message).filter(Message.receiver == username).all()
        db.close()
        return result_messages
    
    db.close()
    raise HTTPException(status_code=400, detail="Username not found")

@app.post("/delete_messages")
def delete_messages(receiver: str):
    db = SessionLocal()
    results = db.query(Message).filter(Message.receiver == receiver).all()

    db.delete(results)

    db.commit()
    db.close()

@app.post("/delete_user")
def delete_user(username: str):
    db = SessionLocal()
    results = db.query(User).filter(User.username == username).first()

    db.delete(results)

    db.commit()
    db.close()