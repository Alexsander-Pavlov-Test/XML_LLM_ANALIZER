from fastapi import APIRouter

from api_v1.renders import render, XMLRender

from config import settings


router = APIRouter(prefix='/products',
                   tags=['Products'],
                   )


@router.get(path='/get-list',
            description='Get list of Products (XML)',
            name='Products XML',
            response_class=XMLRender,
            )
async def get_products_xml():
    return render(
        value=settings.PATH_ITEMS_XML,
        accept='application/xml',
        status_code=200,
        headers=None,
        )
