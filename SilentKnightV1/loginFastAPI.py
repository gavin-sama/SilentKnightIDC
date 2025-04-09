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

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    messages = Column(String)

app = FastAPI()

# Pydantic model
class UserCreate(BaseModel):
    username: str
    password: str
    messages: str

class Message(BaseModel):
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
    db.refresh(new_user)
    db.close()
    return new_user

@app.post("/send_message")
def append_message(message_info: Message):
    db = SessionLocal()

    receiving_user = db.query(User).filter(User.username == message_info.receiver).first()
    if not receiving_user:
        db.close()
        raise HTTPException(status_code=404, detail="Username not found")

    # indices_open_bracket = [i for i in range(len(receiving_user.messages)) if receiving_user.messages[i] == "["]
    # indices_closed_bracket = [i for i in range(len(receiving_user.messages)) if receiving_user.messages[i] == "]"]

    # list_opening = receiving_user.messages[:indices_open_bracket[0]]
    # list_messages = receiving_user.messages[indices_open_bracket[0] + 1:indices_closed_bracket[len(indices_closed_bracket) - 1]]
    # list_closing = receiving_user.messages[indices_closed_bracket[len(indices_closed_bracket) - 1] + 1:]

    # if len(list_messages) == 1:
    #     list_messages = f'"{message_info.message}"'
    # else:
    #     list_messages += f', "{message_info.message}"'

    # receiving_user.messages = list_opening + list_messages + list_closing

    messages_list = json.loads(receiving_user.messages)
    messages_list.append(message_info.message)

    receiving_user.messages = json.dumps(messages_list)

    db.commit()
    db.refresh(receiving_user)
    db.close()

    return receiving_user.messages

@app.get("/messages/{username}")
def read_all_messages(username: str):
    db = SessionLocal()

    valid_user = db.query(User).filter(User.username == username).first()
    if valid_user:
        db.close()
        return valid_user.messages
    
    db.close()
    raise HTTPException(status_code=400, detail="Username not found")

@app.post("/delete_messages")
def delete_messages(username: str):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()

    user.messages = json.dumps([])

    db.commit()
    db.refresh(user)
    db.close()
    return user