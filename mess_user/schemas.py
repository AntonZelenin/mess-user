from pydantic import BaseModel, Field


class UserRegisterData(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=8, max_length=64)


class GetUserIdsByUsernamesRequest(BaseModel):
    usernames: list[str]


class SearchUser(BaseModel):
    user_id: str
    username: str


class SearchUsersResponse(BaseModel):
    users: list[SearchUser]
