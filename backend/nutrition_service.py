
from openai import OpenAI
from backend.models.meal_plan import MealPlan
from backend.goal_strategy import get_goal_strategy

client = OpenAI()


def generate_meal_plan(profile: dict) -> MealPlan:

    goal = profile.get("fitness_goal")

    strategy= get_goal_strategy(goal)

    prompt = f"""
    Create a personalized one-day meal plan.
 
    User profile:
    {profile}

    Fitness Goal:
    {goal}

    Nutrition Strategy:
    {strategy}

    Requirements:
    - Include breakfast, lunch, and dinner.
    - Provide food names for each meal.
    - Estimate calories and macronutrients.
    - Keep recommendations realistic and balanced.
    - Avoid extreme calorie restriction.
    - Ensure daily totals reflect the meals.
    - Nutrition values are estimates, not exact measurements.
    - If the fitness goal is Weight Loss, consider the
      user's current weight, target weight, and timeline.
    - Do not assume the goal is safe or appropriate based
      only on these inputs.
    - Avoid extreme calorie restrictions.
    - Provide balanced meals with adequate nutrition.
    - Nutrition values are estimates.
    """

    response = client.responses.parse(
        model="gpt-4.1-mini",
        instructions=(
            "You are FitAgent AI, a nutrition planning assistant. "
            "Provide general nutrition guidance, not medical advice."
        ),
        input=prompt,
        text_format=MealPlan
    )

    if response.output_parsed is None:
        raise ValueError("Model did not return a valid meal plan")

    return response.output_parsed
