from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username:str
    password:str


class UserInfoBase(BaseModel):
    nick_name:Optional[str] = Field(None,max_length = 50,description="昵称")
    avatar:Optional[str] = Field(None,max_length=500,description="头像")
    gender:Optional[str] = Field(None,max_length=10,description="性别")
    bio:Optional[str] = Field(None,max_length=255,description="简介")

class UserInfoReponse(UserInfoBase):
    id:int
    username:str
    model_config = ConfigDict(from_attributes=True)


class UserAuthResponse(BaseModel):
    token:str
    user_info:UserInfoReponse = Field(...,alias="userInfo"),

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class UserUpdateRequest(UserInfoBase):
    phone:Optional[str] = Field(None,description="手机号")

class UserChangePasswordRequest(BaseModel):
    old_password:str = Field(...,alias="oldPassword",description="旧密码")
    new_password:str = Field(...,alias="newPassword",min_length=6,description="新密码")