from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func

class TimeStampMixin:
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime,default=func.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime,default=func.now,onupdate=func.now)