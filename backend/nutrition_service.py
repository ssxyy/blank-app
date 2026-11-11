from openai import OpenAI
from backend.models.meal_plan import MealPlan, MultiDayMealPlan
from backend.goal_strategy import get_goal_strategy

client = OpenAI()

SYSTEM_INSTRUCTIONS = (
    "You are FitAgent AI, a nutrition planning assistant. "
    "Provide general nutrition guidance, not medical advice."
)

SHARED_REQUIREMENTS = """
    - Provide food names (with rough portions) for each meal.
    - Estimate calories and macronutrients for every meal.
    - Keep recommendations realistic, balanced and affordable.
    - Avoid extreme calorie restriction or crash dieting.
    - Respect the user's dietary preference.
    - If the fitness goal is Weight Loss, consider the
      user's current weight, target weight, and timeline.
    - Do not assume the goal is safe or appropriate based
      only on these inputs.
    - Nutrition values are estimates, not exact measurements.
"""


def generate_meal_plan(profile: dict) -> MealPlan:

    goal = profile.get("fitness_goal")

    strategy = get_goal_strategy(goal)

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
    - Ensure daily totals reflect the meals.
    {SHARED_REQUIREMENTS}
    """

    response = client.responses.parse(
        model="gpt-4.1-mini",
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
        text_format=MealPlan
    )

    if response.output_parsed is None:
        raise ValueError("Model did not return a valid meal plan")

    return response.output_parsed


def generate_multi_day_meal_plan(
    profile: dict,
    days: int
) -> MultiDayMealPlan:

    if days not in (3, 7):
        raise ValueError("Multi-day plans support 3 or 7 days")

    goal = profile.get("fitness_goal")
    strategy = get_goal_strategy(goal)

    prompt = f"""
    Create a personalized {days}-day meal plan.

    User profile:
    {profile}

    Fitness Goal:
    {goal}

    Nutrition Strategy:
    {strategy}

    Requirements:
    - Return exactly {days} days, labelled "Day 1" to "Day {days}".
    - Each day includes Breakfast, Lunch, Dinner and one Snack.
    - Keep each day's calories close (within about 10%) to one
      consistent daily target, and report that target.
    - Each day's daily_calories and daily_protein_g must equal
      the sum of that day's meals.
    - Vary meals across days so the plan does not get repetitive,
      but reuse ingredients so the grocery list stays practical.
    - Provide one consolidated grocery list for all {days} days,
      grouped logically (e.g. "Produce: spinach, bananas").
    - Provide 3-5 short meal-prep / batch-cooking tips.
    {SHARED_REQUIREMENTS}
    """

    response = client.responses.parse(
        model="gpt-4.1-mini",
        instructions=SYSTEM_INSTRUCTIONS,
        input=prompt,
        text_format=MultiDayMealPlan
    )

    plan = response.output_parsed
    if plan is None:
        raise ValueError("Model did not return a valid meal plan")

    if len(plan.days) != days:
        raise ValueError(
            f"Model returned {len(plan.days)} days instead of {days}"
        )

    for day in plan.days:
        day.daily_calories = sum(m.calories for m in day.meals)
        day.daily_protein_g = round(
            sum(m.protein_g for m in day.meals), 1
        )
    plan.plan_days = days

    return plan
