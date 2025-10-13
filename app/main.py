from fastapi import FastAPI
from app.auth import router as auth_router
from app.webhook import router as webhook_router
from app.callback import router as callback_router

app = FastAPI(title="Python Docker Server")

# Register routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(webhook_router, prefix="/webhook", tags=["Webhook"])
app.include_router(callback_router, prefix="/callback", tags=["Callback"])


@app.get("/")
def root():
    return {"message": "Server is running inside Docker!"}
