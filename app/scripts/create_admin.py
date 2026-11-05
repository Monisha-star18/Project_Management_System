
from sqlalchemy import select

from app.core.config import get_settings
from app.core.security import hash_password
from app.database.session import SessionLocal
from app.models.employee import EmployeeData
from app.utilites.logger import logger


async def create_admin() -> None:
    settings = get_settings()

    logger.info("Starting admin creation")

    async with SessionLocal() as session:

        logger.info("Checking existing admin")

        result = await session.execute(
            select(EmployeeData).where(
                EmployeeData.role == "admin"
            )
        )

        logger.info("Admin query completed")

        existing_admin = result.scalar_one_or_none()

        if existing_admin is not None:
            logger.info("Admin already exists")
            return

        if not settings.admin_username or not settings.admin_password:
            raise ValueError("Admin credentials are not configured")

        logger.info("Preparing new admin")

        admin = EmployeeData(
            full_name=settings.admin_username,
            email=settings.admin_email,
            password_hash=hash_password(settings.admin_password),
            role="admin",
            is_active=True
        )

        session.add(admin)

        logger.info("Committing admin")
        await session.commit()

        logger.info("Admin created successfully")
