from typing import List
from pydantic import BaseModel

class MealPlanResponse(BaseModel):
    plans: str

class Nutrition(BaseModel):
    calories: str
    protein: str
    carbs: str
    fats: str


class Meal(BaseModel):
    name: str
    recipeName: str
    recipeThumbnailLink: str
    ingredients: List[str]
    preparation: List[str]
    recipeLink: str
    nutrition: Nutrition


# class DailyTotals(BaseModel):
#     calories: str
#     protein: str
#     carbs: str
#     fats: str


class DietPlan(BaseModel):
    meals: List[Meal]
    dailyTotals: Nutrition


class DietPlanResponse(BaseModel):
    dietPlan: DietPlan