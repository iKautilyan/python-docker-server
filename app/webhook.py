from fastapi import APIRouter, Request, BackgroundTasks
from app.auth import verify_signature
import hmac, hashlib, os, requests

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")


@router.post("/")
async def receive_webhook(request: Request):
    raw = await request.body()
    signature = request.headers.get("x-signature", "")
    if not verify_signature(raw, signature):
        return {"error": "invalid signature"}

    data = await request.json()
    print("Webhook received:", data)
    return {"status": "ok"}
