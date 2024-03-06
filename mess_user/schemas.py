from pydantic import BaseModel, Field


class UserRegisterData(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    password: str = Field(min_length=8, max_length=64)


class GetUsersByIdsRequest(BaseModel):
    user_ids: list[str]


class SearchUserRequest(BaseModel):
    username: str


class User(BaseModel):
    id: str
    username: str


class SearchUsersResponse(BaseModel):
    users: list[User]
