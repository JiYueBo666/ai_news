from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class UserRequest(BaseModel):
    username: str
    password: str


class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=255, description="个人简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    model_config = ConfigDict(
        from_attributes=True,
    )


class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
