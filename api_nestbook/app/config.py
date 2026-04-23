from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MARIADB_HOST: str
    MARIADB_PORT: int
    MARIADB_USER: str
    MARIADB_PASSWORD: str
    MARIADB_DATABASE: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MIN: int    

    model_config = SettingsConfigDict(env_file=".env",env_file_encoding='utf-8',extra='ignore')


settings = Settings()