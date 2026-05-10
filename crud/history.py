from fastapi import Depends
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from models.history import History
from models.news import News


async def add_history(db: AsyncSession, user_id: int, news_id: int) -> History:
    hist = History(user_id=user_id, news_id=news_id)
    db.add(hist)
    await db.commit()
    await db.refresh(hist)
    return hist


async def get_history_list(db: AsyncSession, user_id: int):
    query = (
        select(History, News)
        .join(News, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
    )
    result = await db.execute(query)
    rows = result.all()

    items = []
    for hist, news in rows:
        items.append(
            {
                "id": hist.id,
                "news_id": news.id,
                "title": news.title,
                "image": news.image,
                "author": news.author,
                "view_time": hist.view_time,
            }
        )

    return {"list": items}


async def delete_history(db: AsyncSession, user_id: int, history_id: int) -> bool:
    stmt = delete(History).where(
        History.id == history_id, History.user_id == user_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def clear_history(db: AsyncSession, user_id: int) -> int:
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount
