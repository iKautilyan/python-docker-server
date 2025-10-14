# auth.py
from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter()

# Configuration
HOST_URL = os.getenv("HOST_URL", "https://api.example.com")  # Replace with your actual base URL
API_KEY = os.getenv("API_KEY", "your-api-key")
SOURCE = os.getenv("SOURCE", "web")

# Dummy credentials for testing
USER_ID = os.getenv("USER_ID", "demo_user")
PASSWORD = os.getenv("PASSWORD", "demo_pass")


@router.post("/login")
async def login():
    """
    Authenticate user and return register_token.
    """
    url = f"{HOST_URL}/authentication/v1/user/session"

    payload = {
        "user_id": USER_ID,
        "login_type": "PASSWORD",
        "password": PASSWORD,
        "second_auth_type": "OTP",
        "second_auth": "123456",
        "api_key": API_KEY,
        "source": SOURCE,
        "UDID": "a1b23cd4e5f6g78h",
        "version": "2.0.0",
        "iosversion": "",
        "build_version": "22.11.01",
        "deviceinfo": {
            "UDID": "4ad3f8a8-c90c-4359-9f78-4e8311f77eb2",
            "DeviceModel": "SM-G955U",
            "DeviceManufacturer": "Google Inc.",
            "DevicePlatform": "web",
            "DevicePlatformVer": "Android 8.0.0",
            "AppName": "Wave 2.0",
            "AppVersion": "8.2.21",
            "AppVersionCode": "2000000",
            "AppPackageName": "com.wave.dev",
            "FCMRegKey": "172.25.90.82:8100",
        }
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.post(url, json=payload)
            data = response.json()

            if data.get("status") != "success":
                raise HTTPException(status_code=401, detail=data.get("message", "Auth failed"))

            token = data["data"]["register_token"]
            return {"register_token": token}

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Connection error: {str(e)}")
