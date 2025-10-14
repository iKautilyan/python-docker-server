# orders.py
from fastapi import APIRouter, HTTPException
import httpx
import os

router = APIRouter()
HOST_URL = os.getenv("HOST_URL", "https://api.example.com")

@router.post("/order")
async def place_order(register_token: str):
    """
    Place a sample order using the register_token.
    """
    url = f"{HOST_URL}/transactional/v1/orders/regular"
    headers = {"Authorization": f"Bearer {register_token}"}

    payload = {
        "scrip_info": {
            "exchange": "NCDEX_FO",
            "scrip_token": 54669,
            "symbol": "",
            "series": "",
            "expiry_date": "",
            "strike_price": "",
            "option_type": ""
        },
        "transaction_type": "BUY",
        "product_type": "INTRADAY",
        "order_type": "RL-MKT",
        "quantity": 3,
        "price": 0,
        "trigger_price": 0,
        "disclosed_quantity": 0,
        "validity": "DAY",
        "validity_days": 0,
        "is_amo": False
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            data = response.json()

            if data.get("status") != "success":
                raise HTTPException(status_code=400, detail=data.get("message", "Order failed"))

            return {"order_id": data["data"]["orderId"]}

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Order service error: {str(e)}")
