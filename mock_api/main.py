from fastapi import FastAPI

from db import Base, engine
from routes.routes import router as leave_router
from routes.ai_router import router as ai_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(leave_router)
app.include_router(ai_router)

@app.get("/")
def home():
    return {
        "message": "Leave Management API is running"
    }