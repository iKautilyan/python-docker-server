from fastapi import FastAPI
from app.auth import router as auth_router
from app.orders import router as order_router

app = FastAPI(title="Trading Server")

app.include_router(auth_router)
app.include_router(order_router)

@app.get("/")
def root():
    return {"message": "Python server running!"}
