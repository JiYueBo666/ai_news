from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import news

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def get_categories(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):

    categories = await news.get_categories(db, skip, limit)

    return {"code": 200, "msg": "新闻获取分类成功", "data": categories}


@router.get("/list")
async def get_news_list(
    db: AsyncSession = Depends(get_db),
    page: int = 1,
    page_size: int = Query(..., alias="pageSize"),
    category_id: int = Query(..., alias="categoryId"),
):
    news_list = await news.get_news_list(
        db, page_size=page_size, page=page, category_id=category_id
    )

    total = await news.get_news_count(db, category_id)
    has_more = total > (page - 1) * page_size

    return {
        "code": 200,
        "msg": "新闻列表获取成功",
        "data": {"list": news_list},
        "total": total,
        "has_more": has_more,
    }


@router.get("/detail")
async def get_news_detail(
    db: AsyncSession = Depends(get_db), news_id: int = Query(..., alias="id")
):
    news_datail = await news.get_news_datail(db=db, news_id=news_id)
    if not news_datail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    is_shot = await news.increase_news_view(db=db, news_id=news_datail.id)
    if is_shot == False:
        raise HTTPException(status_code=404, detail="新闻浏览量增加失败")

    related_news = await news.get_related_news(
        db=db, category_id=news_datail.category_id, news_id=news_datail.id, limit=5
    )

    return {
        "code": 200,
        "msg": "success",
        "data": {
            "id": news_datail.id,
            "title": news_datail.title,
            "content": news_datail.content,
            "image": news_datail.image,
            "author": news_datail.author,
            "publishTime": news_datail.publish_time,
            "updateTime": news_datail.updated_at,
            "categoryId": news_datail.category_id,
            "views": news_datail.views,
            "relatedNews": related_news,
        },
    }
