
GOAL_STRATEGIES = {
    "Weight Loss": (
        "Support gradual, sustainable weight loss. "
        "Focus on balanced meals, adequate protein, "
        "fiber, and a modest calorie deficit when appropriate. "
        "Avoid restrictive or crash diets."
    ),

    "Build Muscle": (
        "Support muscle growth with adequate energy, "
        "protein, carbohydrates, and recovery nutrition."
    ),

    "Fat Loss & Muscle Retention": (
        "Support fat loss while preserving muscle. "
        "Prioritize resistance training nutrition, "
        "adequate protein, and a modest calorie deficit."
    ),

    "Maintain Weight": (
        "Support weight maintenance through "
        "balanced nutrition and adequate energy intake."
    ),

    "General Fitness": (
        "Focus on balanced meals, dietary variety, "
        "and overall nutritional quality."
    )
}


def get_goal_strategy(goal: str) -> str:
    return GOAL_STRATEGIES.get(
        goal,
        GOAL_STRATEGIES["General Fitness"]
    )
