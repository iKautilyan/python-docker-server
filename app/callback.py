from fastapi import APIRouter, BackgroundTasks
import requests, hmac, hashlib, os, json

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
CALLBACK_URL = os.getenv("CALLBACK_URL", "https://example.com/receive")

def sign_payload(payload: dict):
    data = json.dumps(payload, separators=(',', ':')).encode()
    sig = hmac.new(SECRET_KEY.encode(), data, hashlib.sha256).hexdigest()
    return sig


def send_callback(payload: dict):
    sig = sign_payload(payload)
    headers = {"x-signature": sig, "Content-Type": "application/json"}
    resp = requests.post(CALLBACK_URL, json=payload, headers=headers)
    print("Callback response:", resp.status_code, resp.text)


@router.post("/")
async def trigger_callback(background_tasks: BackgroundTasks):
    payload = {"message": "This is a test callback"}
    background_tasks.add_task(send_callback, payload)
    return {"status": "callback sent"}
