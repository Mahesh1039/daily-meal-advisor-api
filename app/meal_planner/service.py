import json
from openai import OpenAI
import urllib.request
import urllib.parse
from app.meal_planner.schema import DietPlanResponse
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_RETRIES = os.getenv("MAX_RETRIES")

class MealPlannerService:
    @staticmethod
    def get_meal_plans(meal_type: str, gender: str, weight: int,includeSnacks: bool,requiredCalories:int, attempt: int = 1):

        response = client.responses.parse(
            model=os.getenv("AI_MODEL"),
            prompt={
                "id": os.getenv("AI_PROMPT_ID"),
                "version": os.getenv("AI_PROMPT_VERSION"),
                "variables": {
                    "requiredcalories": str(requiredCalories),
                    "diettype": meal_type,
                    "gender": gender,
                    "weight": str(weight),
                    "includesnacks": 'Yes' if includeSnacks else 'No'                    
                }
            },
            text_format=DietPlanResponse,
            max_output_tokens=2000
        )

        meals = response.output_parsed.dietPlan.meals

        if len(meals) >= 3:
            return response.output_parsed
        elif attempt >= MAX_RETRIES:
            print(f"Warning: Could not get all 3 meals after {MAX_RETRIES} attempts.")
            return response.output_parsed  # return whatever we got
        else:
            print(f"Retrying API call, attempt {attempt}...")
            return MealPlannerService.get_meal_plans(meal_type, gender, weight,includeSnacks, attempt + 1)
        
    @staticmethod
    def get_recipy_images(recipy_title):
        url = "https://www.googleapis.com/customsearch/v1"
        cx = os.getenv("GOOGLE_CUSTOM_SEARCH_CX")
        google_api_key = os.getenv("GOOGLE_API_KEY")

        encoded_query = urllib.parse.quote(recipy_title + " recipe dish photo")

        url = f"https://www.googleapis.com/customsearch/v1?q={encoded_query}&searchType=image&num=1&key={google_api_key}&cx={cx}"
    
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        
        if "items" in data:
            image_url = data["items"][0]["link"]
            # print("Found Image URL: ----------------------- ", image_url)
            return image_url
        else:
            # print("Found Image URL: ------------------------ NOT FOUND")
            return ""
    

