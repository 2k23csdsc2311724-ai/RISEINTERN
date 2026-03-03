from pymongo import MongoClient
from datetime import datetime
import bcrypt  # example password-hasher

client = MongoClient("mongodb://localhost:27017/")
db = client["riseintern"]
users = db["users"]
users.create_index("email", unique=True)

def register_user(username, email, plain_password):
    pw_hash = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    user_doc = {
        "username": username,
        "email": email,
        "password_hash": pw_hash,
        "signup_date": datetime.utcnow(),
        # add more optional fields...
    }
    try:
        result = users.insert_one(user_doc)
        print("Registered new user with id:", result.inserted_id)
    except Exception as e:
        print("Error — maybe user/email already exists:", e)

# Example usage
register_user("alice123", "alice@example.com", "mysecretpassword")
