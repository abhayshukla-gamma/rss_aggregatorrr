from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.sql import func

from app.core.database import Base
from app.models import feed


class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), index=True)
    title = Column(String, nullable=False)
    link = Column(String, unique=True, nullable=False)
    published = Column(String)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
