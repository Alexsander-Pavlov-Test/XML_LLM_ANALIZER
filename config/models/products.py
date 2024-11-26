from sqlalchemy.orm import Mapped
from datetime import date

from config.models import Base


class Product(Base):
    """
    Модель продукта
    """
    date: Mapped[date]
    name: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[float]
    category: Mapped[str]
