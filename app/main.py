from fastapi import FastAPI
# from fastapi import FastAPI
from app.database.database import engine
from app.routers.auth import router as auth_router
app = FastAPI(
    title="AI Travel Planner",
    description="Backend API",
    version="1.0.0"
)
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "AI Travel Planner Backend Running 🚀"
    }