from fastapi import APIRouter, Header, HTTPException, Request
import hmac, hashlib, os

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")


def verify_signature(request_body: bytes, signature: str):
    computed = hmac.new(SECRET_KEY.encode(), request_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, signature)


@router.post("/verify")
async def verify_request(request: Request, x_signature: str = Header(None)):
    body = await request.body()
    if not verify_signature(body, x_signature or ""):
        raise HTTPException(status_code=401, detail="Invalid signature")
    return {"status": "verified"}
