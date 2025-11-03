import os
import requests
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Authentication"])

BASE_URL = os.getenv("BASE_URL")
LOGIN_URL = f"{BASE_URL}/authentication/v1/user/session"

@router.api_route("/login", methods=["GET", "POST"])
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
        "x-api-key": API_KEY,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }


    try:
        res = requests.post(LOGIN_URL, json=payload, headers=headers)
        print("DEBUG STATUS:", res.status_code)
        print("DEBUG TEXT:", res.text)
        try:
            data = res.json()
        except Exception:
            return {"error": "Non-JSON response from API", "body": res.text}
        if res.status_code != 200 or "data" not in data:
            return {"error": "Login failed", "details": data}

        access_token = data["data"].get("register_token", None)
        return {"status": "success", "access_token": access_token}

    except Exception as e:
        return {"error": str(e)}
