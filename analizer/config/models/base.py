from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            declared_attr,
                            )
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    """Базовая модель
    """
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    uid: Mapped[int] = mapped_column(primary_key=True)
