# Imports
from pydantic import BaseSettings

# Pydantic Model/Schema for Environment Variables
class Settings(BaseSettings):
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    database_hostname: str

    class Config:
        env_file = ".env" # Getting Environment Variables from ".env" file

# Instance of "Settings" class
settings = Settings()