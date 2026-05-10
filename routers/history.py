from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from crud import history
from crud.users import verify_token
from models.users import User
from schemas.history import HistoryRequest
from utils.response import success_response

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
    req: HistoryRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失效"
        )
    result = await history.add_history(db, user.id, req.newsId)
    return success_response(code=200, msg="添加浏览历史成功", data={"id": result.id})


@router.get("/list")
async def get_history_list(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失效"
        )
    data = await history.get_history_list(db, user.id)
    return success_response(code=200, msg="获取浏览历史成功", data=data)


@router.delete("/delete/{history_id}")
async def delete_history(
    history_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失效"
        )
    ok = await history.delete_history(db, user.id, history_id)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="历史记录不存在"
        )
    return success_response(code=200, msg="删除浏览历史成功")


@router.delete("/clear")
async def clear_history(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(verify_token),
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="登录失效"
        )
    count = await history.clear_history(db, user.id)
    return success_response(code=200, msg=f"已清空 {count} 条浏览历史")
