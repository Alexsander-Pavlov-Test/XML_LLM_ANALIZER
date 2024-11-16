from fastapi import APIRouter


router = APIRouter(prefix='/products',
                   tags=['Products'],
                   )


@router.get(path='/get-list',
            description='Get list of Products (XML)',
            name='Products XML'
            )
async def get_products_xml():
    pass
