from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import favorite
from crud.users import verify_token
from models.users import User
from schemas.favorite import FavoriteRequest
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.get("/check")
async def check_favorite_status(
    news_id: int = Query(..., alias="newsId"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失效"
        )
    is_fav = await favorite.check_favorite(db, user.id, news_id)
    return success_response(
        code=200, msg="success", data={"isFavorite": is_fav}
    )


@router.post("/add")
async def add_favorite(
    req: FavoriteRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失效"
        )
    result = await favorite.add_favorite(db, user.id, req.newsId)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="已收藏"
        )
    return success_response(code=200, msg="收藏成功", data={"id": result.id})


@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失效"
        )
    ok = await favorite.remove_favorite(db, user.id, news_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="收藏不存在"
        )
    return success_response(code=200, msg="取消收藏成功")


@router.get("/list")
async def get_favorite_list(
    page: int = Query(1),
    page_size: int = Query(10, alias="pageSize"),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失效"
        )
    data = await favorite.get_favorite_list(db, user.id, page, page_size)
    return success_response(code=200, msg="获取收藏列表成功", data=data)


@router.delete("/clear")
async def clear_favorites(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失效"
        )
    count = await favorite.clear_favorites(db, user.id)
    return success_response(code=200, msg=f"已清空 {count} 条收藏")
