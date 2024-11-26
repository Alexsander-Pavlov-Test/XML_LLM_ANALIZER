import pytest
from datetime import date

from api_v1.products.dao import ProductDAO


class TestProducts:
    """
    Тесты продуктов
    """

    @pytest.mark.asyncio
    async def test_create_product(self, client, get_async_session):
        product = await ProductDAO.add(
            session=get_async_session,
            date=date(2024, 1, 1),
            name='product',
            quantity=4,
            price=1400.0,
            category='Category',
        )
        assert product.name == 'product'
