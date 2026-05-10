from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FavoriteRequest(BaseModel):
    newsId: int


class FavoriteCheckResponse(BaseModel):
    isFavorite: bool = False
    model_config = ConfigDict(from_attributes=True)


class FavoriteItem(BaseModel):
    id: int
    news_id: int
    title: str
    image: str | None = None
    author: str | None = None
    publish_time: datetime | None = None
    favorite_time: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class FavoriteListResponse(BaseModel):
    list: list[FavoriteItem]
    total: int
    page: int
    page_size: int
