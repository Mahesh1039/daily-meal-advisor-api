from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException
from app.meal_planner.schema import DietPlanResponse
from app.meal_planner.service import MealPlannerService


router = APIRouter()

@router.get("/meal-plan/{meal_type}/{gender}/{weight}/{includeSnacks}/{requiredCalories}", response_model=DietPlanResponse)
def get_meal_plan(meal_type: str, gender: str, weight: int,includeSnacks:bool,requiredCalories: int):
    try:
        dietPlan: DietPlanResponse = MealPlannerService.get_meal_plans(meal_type,gender,weight,includeSnacks,requiredCalories)

        for meal in dietPlan.dietPlan.meals:
            thumbnailLink = MealPlannerService.get_recipy_images(meal.recipeName)
            meal.recipeThumbnailLink = thumbnailLink

        return dietPlan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
