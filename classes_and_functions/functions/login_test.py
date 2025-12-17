import json
from dotenv import load_dotenv
import os

load_dotenv()

def read_data():
    
    data=None
    with open('static/utils/data.json', 'r') as f:
        data = json.load(f)
    return data

def test_login(email,password):
    data = {
        "email": os.getenv("email"),
        "password": os.getenv("password")
    }
    if(data["email"]==email and data["password"]==password):
        return True
    return False
