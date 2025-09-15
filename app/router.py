from fastapi import APIRouter
from app.meal_planner import router as meal_planner_router

router = APIRouter()

router.include_router(meal_planner_router.router, tags=["meal planner"])