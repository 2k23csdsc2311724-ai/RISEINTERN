# backend/app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from datetime import datetime
import bcrypt

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["riseintern"]
users = db["users"]

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str     # plaintext — we'll hash it

@app.post("/api/signup")
def signup(user: UserSignup):
    # check if email already exists
    if users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    pw_hash = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    user_doc = {
        "username": user.username,
        "email": user.email,
        "password_hash": pw_hash,
        "signup_date": datetime.utcnow()
    }
    result = users.insert_one(user_doc)
    return {"status": "success", "user_id": str(result.inserted_id)}
