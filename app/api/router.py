from fastapi import APIRouter

from .routes.filter import router as filter_router
from .routes.explainer import router as explainer_router
from .routes.agent import router as agent_router


api_router = APIRouter()

api_router.include_router(filter_router)
api_router.include_router(explainer_router)
api_router.include_router(agent_router)