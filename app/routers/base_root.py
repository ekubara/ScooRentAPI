from fastapi import APIRouter

from app.types.models.base import APIData


router = APIRouter(tags=['base'])


@router.get('/', response_model=APIData)
async def load_base_root():
    """Return api data."""

    return APIData()
