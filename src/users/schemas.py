from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str | None = None
    password: str


class UserRead(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None