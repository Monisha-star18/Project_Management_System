
from sqlalchemy import select
from sqlalchemy.engine import Result

from app.core.config import get_settings
from app.core.security import hash_password
from app.database.session import SessionLocal
from app.models.employee import EmployeeData
from app.utilites.logger import logger


async def create_admin() -> None:
    settings = get_settings()

    async with SessionLocal() as session:

        result: Result = await session.execute(
            select(EmployeeData).where( EmployeeData.role == "admin" )
        )

        existing_admin: EmployeeData | None = result.scalar_one_or_none()

        if existing_admin is not None:
            logger.info("Admin already exists")
            return

        if not settings.admin_username or not settings.admin_password:
            logger.warning("Admin credentials are not configured")
            raise ValueError("Admin credentials are not configured")
        

        admin: EmployeeData = EmployeeData(
            full_name = settings.admin_username,
            email = settings.admin_email,
            password_hash=hash_password(settings.admin_password),
            role="admin",
            is_active=True
        )

        session.add(admin)
        await session.commit()

        logger.info("Admin created successfully")
