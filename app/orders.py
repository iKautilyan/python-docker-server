import os
import requests
from fastapi import APIRouter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/order", tags=["Orders"])

BASE_URL = os.getenv("BASE_URL")
ORDER_URL = f"{BASE_URL}/transactional/v1/orders/regular"

def get_headers(token):
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "x-api-key": os.getenv("API_KEY")
    }

@router.post("/buy")
def buy_order(token: str):
    payload = {
        "scrip_info": {
            "exchange": "NSE_FO",
            "symbol": "OPTION_SYMBOL",
            "series": "OPT",
            "expiry_date": "2025-12-31",
            "strike_price": "10000",
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

    res = requests.post(ORDER_URL, json=payload, headers=get_headers(token))
    return res.json()

@router.post("/sell")
def sell_order(token: str):
    payload = {
        "scrip_info": {
            "exchange": "NSE_FO",
            "symbol": "OPTION_SYMBOL",
            "series": "OPT",
            "expiry_date": "2025-12-31",
            "strike_price": "10000",
            "option_type": "CE"
        },
        "transaction_type": "SELL",
        "product_type": "INTRADAY",
        "order_type": "RL-MKT",
        "quantity": 1,
        "price": 0,
        "trigger_price": 0,
        "validity": "DAY"
    }

    res = requests.post(ORDER_URL, json=payload, headers=get_headers(token))
    return res.json()
