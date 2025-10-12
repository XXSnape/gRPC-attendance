from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, PostgresDsn, MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()


class RunConfig(BaseModel):
    """
    Конфигурация для запуска приложения.
    """

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    grpc_server_host: str = "localhost"
    grpc_server_port: int = 50051

    @property
    def grpc_url(self):
        return f"{self.grpc_server_host}:{self.grpc_server_port}"


class ApiV1Prefix(BaseModel):
    """
    Префиксы для API версии 1.
    """

    prefix: str = "/v1"
    users: str = "/users"


class ApiPrefix(BaseModel):
    """
    Конфигурация префиксов для API.
    """

    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class MongoDBConfig(BaseSettings):
    """
    Конфигурация MongoDB.
    """

    mongo_user: str
    mongo_password: str
    mongo_host: str
    mongo_port: int

    @property
    def url(self) -> MongoDsn:
        """
        Возвращает строку для подключения к MongoDB.
        """
        return MongoDsn(
            f"mongodb://{self.mongo_user}:"
            f"{self.mongo_password}@{self.mongo_host}:{self.mongo_port}"
        )


class DatabaseConfig(BaseSettings):
    """
    Конфигурация базы данных.
    """

    db_host: str
    db_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    echo: bool = False

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @property
    def url(self) -> PostgresDsn:
        """
        Возвращает строку для подключения к базе данных.
        """
        return PostgresDsn(
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.db_host}:{self.db_port}/{self.postgres_db}"
        )


class Settings(BaseSettings):
    """
    Основные настройки приложения.
    """

    run: RunConfig = RunConfig()
    db: DatabaseConfig = DatabaseConfig()
    mongo_db: MongoDBConfig = MongoDBConfig()
    api: ApiPrefix = ApiPrefix()
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )


settings = Settings()
