from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.database_conf import get_db
from crud.users import create_token, update_user, update_password
from models.users import User
from schemas.users import UserRequest, UserInfoReponse, UserUpdateRequest, UserChangePasswordRequest

from crud import users
from schemas.users import UserAuthResponse
from utils.auth import get_current_user
from utils.response import success_response
router = APIRouter(prefix="/api/user",tags=["users"])

@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession = Depends(get_db),):

    existing_user = await users.get_user_by_username(db,user_data.username)

    if existing_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST,detail = "用户已存在")

    user = await users.create_user(db,user_data)

    token = await users.create_token(db,user.id)
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": token,
    #         "userInfo": {
    #           "id": user.id,
    #           "username": user.username,
    #           "bio": user.bio,
    #           "avatar": user.avatar
    #         }
    #     }
    # }
    #
    user_info = UserInfoReponse.model_validate(user)
    response_data = UserAuthResponse(token = token,user_info = user_info)
    return success_response("注册成功",response_data)


@router.post("/login")
async def login_user(user_data:UserRequest,db:AsyncSession = Depends(get_db)):
    user = await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    user_info = UserInfoReponse.model_validate(user)
    response_data = UserAuthResponse(token=token, user_info=user_info)
    return success_response("登陆成功",response_data)

@router.get("/info")
async def get_user_info(user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    data = UserInfoReponse.model_validate(user)
    return success_response("获取用户信息成功",data)

@router.put("/update")
async def update_user_info(user_data:UserUpdateRequest,
                           user:User = Depends(get_current_user),
                           db:AsyncSession = Depends(get_db)):
    user = await update_user(db,user.username,user_data)
    data = UserInfoReponse.model_validate(user)
    return success_response("修改用户信息成功",data)


@router.put("/password")
async def update_user_password(
        password_data:UserChangePasswordRequest,
        user:User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)
):
    res_change_pwd = await update_password(db,user,password_data.old_password,password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="修改密码失败")


    return success_response("修改用户信息成功")


