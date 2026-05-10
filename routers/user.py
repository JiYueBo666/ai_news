from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.users import User
from schemas.user import UserAuthResponse, UserInfoResponse, UserRequest
from crud.users import (
    check_password,
    create_user,
    get_user_by_username,
    create_token,
    has_register,
    verify_token,
)
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/register")
async def register_user(user_data: UserRequest, db: AsyncSession = Depends(get_db)):

    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在"
        )

    user = await create_user(db, user_data)
    token = await create_token(db, user.id)

    return success_response(
        code=200,
        msg="注册成功",
        data=UserAuthResponse(
            token=token, userInfo=UserInfoResponse.model_validate(user)
        ),
    )


@router.post("/login")
async def login_user(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    user_info = await has_register(user_data, db)
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    password_check = await check_password(user_data, user_info)
    if not password_check:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    token = await create_token(db, user_info.id)
    return success_response(
        code=200,
        msg="登录成功",
        data=UserAuthResponse(
            token=token, userInfo=UserInfoResponse.model_validate(user_info)
        ),
    )


@router.get("/info")
async def get_user_info(user: User = Depends(verify_token)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失效")
    return success_response(
        code=200,
        msg="获取用户信息成功",
        data=UserInfoResponse(
            id=user.id,
            username=user.username,
        ),
    )
