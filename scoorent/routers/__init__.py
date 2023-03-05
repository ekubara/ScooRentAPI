from fastapi import APIRouter

from . import admins
from . import base_root
from . import users
from . import scooters
from scoorent.security import jwt_processor


router = APIRouter()

# include all sub routers
router.include_router(admins.router)
router.include_router(base_root.router)
router.include_router(users.router)
router.include_router(scooters.router)
router.include_router(jwt_processor.router)
