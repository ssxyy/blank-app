from pydantic import BaseModel,Field

class Meal(BaseModel):
    meal_name: str = Field(
        description = 'Name of your meal , such as Breakfast'
    )

    foods: list[str] = Field(
        description="list of foods included in the meal"
    )

    calories: int = Field(
        description="Estimated protein in grams"
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