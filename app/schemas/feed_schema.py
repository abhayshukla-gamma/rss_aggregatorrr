from pydantic import BaseModel, HttpUrl  # check automatically


class FeedCreate(BaseModel):
    title: str
    url: HttpUrl
