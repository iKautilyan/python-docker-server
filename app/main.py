from fastapi import FastAPI
from auth import router as auth_router
from orders import router as order_router

app = FastAPI()

app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(order_router, prefix="/api", tags=["orders"])

@app.get("/")
def home():
    return {"message": "Python server is running locally!"}
