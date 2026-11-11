from pydantic import BaseModel, Field


class Meal(BaseModel):
    meal_name: str = Field(
        description="Name of the meal, such as Breakfast"
    )

    foods: list[str] = Field(
        description="List of foods included in the meal"
    )

    calories: int = Field(
        description="Estimated calories (kcal)"
    )

    protein_g: float = Field(
        description="Estimated protein in grams"
    )

    carbs_g: float = Field(
        description="Estimated carbohydrates in grams"
    )

    fat_g: float = Field(
        description="Estimated fat in grams"
    )


class MealPlan(BaseModel):
    daily_calories: int
    daily_protein_g: float
    meals: list[Meal]


class DayMealPlan(BaseModel):
    day: str = Field(
        description="Label for the day, e.g. 'Day 1'"
    )
    daily_calories: int = Field(
        description="Sum of calories for all meals on this day"
    )
    daily_protein_g: float = Field(
        description="Sum of protein for all meals on this day"
    )
    meals: list[Meal]


class MultiDayMealPlan(BaseModel):
    plan_days: int = Field(
        description="Number of days in the plan (3 or 7)"
    )
    target_daily_calories: int = Field(
        description="Approximate daily calorie target the plan aims for"
    )
    target_daily_protein_g: float = Field(
        description="Approximate daily protein target in grams"
    )
    days: list[DayMealPlan]
    grocery_list: list[str] = Field(
        description="Consolidated shopping list for the whole plan"
    )
    prep_tips: list[str] = Field(
        description="Short batch-cooking or meal-prep tips for the plan"
    )
