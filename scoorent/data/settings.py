from os import getcwd

from pydantic import BaseSettings


class SecuritySettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class ProjectSettings(BaseSettings):
    data_directory: str = getcwd() + "/data/"
    env_file: str = data_directory + ".env"


class DatabaseSettings(BaseSettings):
    username: str
    password: str
    database_name: str


project_settings = ProjectSettings()
security_settings = SecuritySettings(_env_file=project_settings.env_file)
database_settings = DatabaseSettings(_env_file=project_settings.env_file)
