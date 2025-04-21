from aiogram import Router

from .handler.start_help import router as start_help_router
from .handler.catalog import router as catalog_router
from .handler.register import router as register_router
from .handler.contacts import router as contacts_router
from .handler.cart import router as cart_router


router = Router()

router.include_router(start_help_router)
router.include_router(catalog_router)
router.include_router(register_router)
router.include_router(contacts_router)
router.include_router(cart_router)