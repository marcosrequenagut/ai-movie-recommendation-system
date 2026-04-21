from fastapi import APIRouter

from routes.recommendation import router as recommendation_router
from routes.filter import router as filter_router

api_router = APIRouter()

api_router.include_router(filter_router)
api_router.include_router(recommendation_router)