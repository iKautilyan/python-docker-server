import os
import requests
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Authentication"])

BASE_URL = os.getenv("BASE_URL")
LOGIN_URL = f"{BASE_URL}/authentication/v1/user/session"

@router.post("/login")
def login_user():
    payload = {
        "user_id": os.getenv("USER_ID"),
        "login_type": "PASSWORD",
        "password": os.getenv("PASSWORD"),
        "second_auth_type": "OTP",
        "second_auth": os.getenv("OTP"),
        "api_key": os.getenv("API_KEY"),
        "source": os.getenv("SOURCE"),
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.getenv("API_KEY")
    }

    res = requests.post(LOGIN_URL, json=payload, headers=headers)
    data = res.json()

    if res.status_code != 200 or "data" not in data:
        return {"error": "Login failed", "details": data}

    access_token = data["data"].get("register_token", None)
    return {"status": "success", "access_token": access_token}
