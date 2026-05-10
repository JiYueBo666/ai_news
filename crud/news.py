from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category
from models.news import News


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()
    return categories


async def get_news_list(db: AsyncSession, page_size: int, page: int, category_id: int):
    query = (
        select(News)
        .where(News.category_id == category_id)
        .offset(page_size * (page - 1))
        .limit(page_size)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_news_count(db: AsyncSession, category_id: int):
    query = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(query)
    return result.scalar_one()  # 只能有一个结果，否则报错


async def get_news_datail(db: AsyncSession, news_id: int):
    query = select(News).where(News.id == news_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def increase_news_view(db: AsyncSession, news_id: int):
    query = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(query)
    await db.commit()

    # 检查
    return result.rowcount > 0


async def get_related_news(
    db: AsyncSession, news_id: int, category_id: int, limit: int = 5
):
    query = (
        select(News)
        .where(News.category_id == category_id, News.id != news_id)
        .limit(limit)
        .order_by(News.views.desc(), News.publish_time.desc())
    )
    result = await db.execute(query)
    return [
        {
            "id": news_datail.id,
            "title": news_datail.title,
            "content": news_datail.content,
            "image": news_datail.image,
            "author": news_datail.author,
            "publishTime": news_datail.publish_time,
            "updateTime": news_datail.updated_at,
            "categoryId": news_datail.category_id,
            "views": news_datail.views,
        }
        for news_datail in result.scalars().all()
    ]
