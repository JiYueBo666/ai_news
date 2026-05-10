from datetime import datetime, timedelta
import uuid

from fastapi import Depends
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from models.users import User, UserToken
from schemas.user import UserRequest
from utils.security import get_token, hash_password, verify_password


async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user_data: UserRequest):
    hashed_password = hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


# 生产token
async def create_token(db: AsyncSession, user_id: int):
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    # 查有没有token
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    # 有则更新，无则赋值
    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
    await db.commit()
    return token


async def has_register(user_data: UserRequest, db: AsyncSession):
    query = select(User).where(User.username == user_data.username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def check_password(user_data: UserRequest, select_data: User):
    password = user_data.password
    return verify_password(password, select_data.password)


async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def verify_token(
    db: AsyncSession = Depends(get_db), token: str = Depends(get_token)
):
    if not token:
        return None
    query = select(UserToken).where(
        and_(UserToken.token == token, UserToken.expires_at > datetime.now())
    )
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if not user_token:
        return None
    query = select(User).where(User.id == user_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()
