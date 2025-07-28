# Structured Output Model (Pydantic)
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class NewsSummary(BaseModel):
    title: str
    url: HttpUrl
    summary: str
    published_at: datetime
    source: str
