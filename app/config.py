from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str 
    database_port: str = None
    database_password: str = None
    database_username: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = '.env'

settings = Settings()
