from pydantic import BaseModel
from pydantic import ConfigDict


class User(BaseModel):
    name: str


class Category(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)