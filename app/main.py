from fastapi import FastAPI

from app.core.config import get_settings 
from app.api.routers.health import router as health_router

setting = get_settings()


app=FastAPI(
    title=setting.app_name,
    description="Project Management System API for managing employees, projects, tasks, and project progress.",
    version="1.0.0",
)

app.include_router(health_router)



@app.get(
    "/",
    tags=["Root"],
    summary="Welcome API",
    description="Returns a welcome message for the Project Management System."
)
async def root() -> dict[str,str]:
    return {
        "message": "Welcome to Project Management System API"
    }