import os
import httpx
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

router = APIRouter()

# Environment variables
BASE_URL = os.getenv("BASE_URL", "https://www.synapsewave.com/api/b2capi")
API_KEY = os.getenv("API_KEY", "")
USER_ID = os.getenv("USER_ID", "")
PASSWORD = os.getenv("PASSWORD", "")
SOURCE = os.getenv("SOURCE", "WEBAPI")
OTP = os.getenv("OTP", "123456")

LOGIN_URL = f"{BASE_URL}/authentication/v1/user/session"
ORDER_URL = f"{BASE_URL}/transactional/v1/orders/regular"


@router.post("/auth/login")
async def login_user():
    """Authenticate user and get access token"""
    payload = {
        "user_id": USER_ID,
        "login_type": "PASSWORD",
        "password": PASSWORD,
        "second_auth_type": "OTP",
        "second_auth": OTP,
        "api_key": API_KEY,
        "source": SOURCE,
        "UDID": "a1b23cd4e5f6g78h",
        "version": "2.0.0",
        "deviceinfo": {
            "DevicePlatform": "web",
            "DeviceManufacturer": "Google Inc.",
            "AppName": "Wave 2.0",
            "AppVersion": "8.2.21"
        }
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(LOGIN_URL, json=payload, headers=headers)

        # Handle ModSecurity / HTML responses gracefully
        if res.headers.get("content-type", "").startswith("text/html"):
            raise HTTPException(
                status_code=406,
                detail="ModSecurity blocked this request. Try adding a User-Agent or test locally."
            )

        data = res.json()
        if res.status_code != 200 or data.get("status") != "success":
            raise HTTPException(status_code=400, detail=data)

        print("✅ LOGIN SUCCESS:", data)
        return {"access_token": data["data"].get("register_token", ""), "full_response": data}

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {e}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Response parsing error: {e}")


@router.post("/order")
async def place_order():
    """Place a sample order"""
    access_token = os.getenv("ACCESS_TOKEN", "")  # Optionally store token in env
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
        "x-api-key": API_KEY,
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/123.0.0.0 Safari/537.36"
        )
    }

    payload = {
        "scrip_info": {
            "exchange": "NSE_FO",
            "symbol": "OPTION_SYMBOL",
            "series": "OPT",
            "expiry_date": "YYYY-MM-DD",
            "strike_price": "PRICE",
            "option_type": "CE"
        },
        "transaction_type": "BUY",
        "product_type": "INTRADAY",
        "order_type": "RL-MKT",
        "quantity": 1,
        "price": 0,
        "trigger_price": 0,
        "validity": "DAY"
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            res = await client.post(ORDER_URL, json=payload, headers=headers)

        if res.headers.get("content-type", "").startswith("text/html"):
            raise HTTPException(
                status_code=406,
                detail="ModSecurity blocked this request. Try testing locally or whitelisting your IP."
            )

        data = res.json()
        print("✅ ORDER RESPONSE:", data)
        return data

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {e}")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"Response parsing error: {e}")
