from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str


class UserIn(UserBase):
    name: str
    #email: str
    #phone: str


class UserDb(UserIn):
    id: int


class UserLoginIn(UserBase):
    pass



