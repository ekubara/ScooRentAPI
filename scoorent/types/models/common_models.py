from pydantic import BaseModel


class GoodResponse(BaseModel):
    ok: bool = True
