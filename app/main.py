from fastapi import FastAPI
from app.auth import router as auth_router
from app.orders import router as order_router

app = FastAPI(title="FastAPI Docker Server")

# Include routers
app.include_router(auth_router, prefix="/api", tags=["auth"])
app.include_router(order_router, prefix="/api", tags=["orders"])

@app.get("/")
def home():
    return {"message": "Python server is running inside Docker!"}
