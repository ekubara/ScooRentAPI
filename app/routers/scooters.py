from fastapi import APIRouter


router = APIRouter(prefix='/scooters')


@router.get('/', tags=['scooters'])
async def process_scooters_base_root():
    """Process user's query to load scooters base root."""

    return "/scooters/ is 200 :)"
