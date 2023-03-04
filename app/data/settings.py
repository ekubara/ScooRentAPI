from os import getcwd

from pydantic import BaseSettings


class SecuritySettings(BaseSettings):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class ProjectSettings(BaseSettings):
    data_directory: str = getcwd() + "/data/"


project_settings = ProjectSettings()
security_settings = SecuritySettings(
    _env_file=project_settings.data_directory+'.env',
    _env_file_encoding='utf-8'
)
