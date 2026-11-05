from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session

router = APIRouter(
    prefix="/api/health",
    tags=["Health"]
)

@router.get(
    "/",
    summary="Health Check",
    description="Check whether the FastAPI application is running successfully.",
)
async def health_check()->dict[str,str]:
    return{
        "status": "success",
        "message": "API is running"
    }

@router.get(
    "/db",
    summary="Database Health Check",
    description="Checks PostgreSQL database connectivity."
)
async def database_health_check(db: Annotated[AsyncSession, Depends(get_session)],)->dict[str,str]:

    await db.execute(text("SELECT 1"))

    return {
        "status": "success",
        "message": "Database connected successfully"
    }
