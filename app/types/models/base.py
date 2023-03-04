from pydantic import BaseModel


class APIData(BaseModel):
    developer: str = "nochanga"
    description: str = "This API made to manage your passwords. Fast, easy and safety. Nothing else."
    version: float | int = 0.1
