from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class URLCreate(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    id: int
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True


class URLStats(BaseModel):
    short_code: str
    original_url: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
