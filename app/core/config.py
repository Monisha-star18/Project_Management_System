from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

class Settings(BaseSettings):
    app_name: str = "Project Management System API"

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str
    db_user: str
    db_password: str

    test_db_name :str

    admin_username: str 
    admin_password: str 
    admin_email: str
    admin_role : str
    
    security_key :str = Field(validation_alias="JWT_SECRET_KEY")
    algorithm : str = Field(validation_alias="JWT_ALGORITHM")
    expire_time : int = Field(validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    mailjet_api_key: str
    mailjet_secret_key: str
    mailjet_sender_email: str
    mailjet_sender_name: str 

    team_lead_sender_email: str

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )

    @property
    def test_database_url(self) -> URL:
            return URL.create(
                drivername="postgresql+asyncpg",
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.test_db_name,
            )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()