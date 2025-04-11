# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # PostgreSQL
    postgres_host: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_port: int

    # Firebird
    firebird_host: str
    firebird_database: str
    firebird_user: str
    firebird_password: str

    # JWT / Autenticação
    JWT_SECRET_KEY: str = "changeme"  # 🔐 Substituir no .env em produção!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # tempo em minutos (1h)

    # Configuração do carregamento de variáveis .env
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Retorna a URI para conexão com o banco PostgreSQL principal."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def TEST_DATABASE_URL(self) -> str:
        """Retorna a URI para conexão com o banco de testes PostgreSQL."""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}_test"
        )


# Instância global de configurações
settings = Settings()
# Para acessar as variáveis de configuração em qualquer parte do código, use:
# settings.postgres_host, settings.SECRET_KEY, etc.