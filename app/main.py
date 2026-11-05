from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import get_settings 
from app.api.routers.health import router as health_router
from app.api.routers.employee import router as employee_router
from app.api.routers.auth import router as auth_router
from app.api.routers.project import router as project_router
from app.api.routers.project_allotment import router as project_allotment_router
from app.api.routers.task import router as task_router
from app.api.routers.report import router as report_router

from app.exceptions.base_exception import AppException
from app.exceptions.handlers import app_exception_handler
from app.utilites.logger import logger
from app.middleware.logging_middleware import LoggingMiddleware

from app.scripts.create_admin import create_admin

setting = get_settings()

#lifespane 
@asynccontextmanager
async def lifespan(app:FastAPI):

    logger.info("Project Management System started")
    await create_admin()

    yield

    logger.info("Project Management System stopped")


app=FastAPI(
    title=setting.app_name,
    description="Project Management System API for managing employees, projects, tasks, and project progress.",
    version="1.0.0",
    lifespan=lifespan
)

#middleware
app.add_middleware(LoggingMiddleware)

#base router 
@app.get(
    "/",
    tags=["Root"],
    summary="Welcome API",
    description="Returns a welcome message for the Project Management System."
)
async def root() -> dict[str,str]:
    return { "message": "Welcome to Project Management System API"}


#routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(project_router)
app.include_router(project_allotment_router)
app.include_router(task_router)
app.include_router(report_router)

# Register global exception handler
app.add_exception_handler(
    AppException,
    app_exception_handler 
)

