from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HistoryRequest(BaseModel):
    newsId: int


class HistoryItem(BaseModel):
    id: int
    news_id: int
    title: str
    image: str | None = None
    author: str | None = None
    view_time: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class HistoryListResponse(BaseModel):
    list: list[HistoryItem]
