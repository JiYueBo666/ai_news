from fastapi import Depends
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud.users import verify_token
from models.favorite import Favorite
from models.news import News
from models.users import User


async def check_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    query = select(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


async def add_favorite(db: AsyncSession, user_id: int, news_id: int) -> Favorite | None:
    exists = await check_favorite(db, user_id, news_id)
    if exists:
        return None
    fav = Favorite(user_id=user_id, news_id=news_id)
    db.add(fav)
    await db.commit()
    await db.refresh(fav)
    return fav


async def remove_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    stmt = delete(Favorite).where(
        Favorite.user_id == user_id, Favorite.news_id == news_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def clear_favorites(db: AsyncSession, user_id: int) -> int:
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount


async def get_favorite_list(
    db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10
):
    query = (
        select(Favorite, News)
        .join(News, Favorite.news_id == News.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()

    count_query = select(func.count(Favorite.id)).where(
        Favorite.user_id == user_id
    )
    total = await db.execute(count_query)
    total = total.scalar_one()

    items = []
    for fav, news in rows:
        items.append(
            {
                "id": news.id,
                "news_id": news.id,
                "title": news.title,
                "image": news.image,
                "author": news.author,
                "publish_time": news.publish_time,
                "favorite_time": fav.created_at,
            }
        )

    return {"list": items, "total": total, "page": page, "page_size": page_size}
