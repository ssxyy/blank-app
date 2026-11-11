from openai import OpenAI
import time

client = OpenAI()

MODEL = "gpt-4.1-mini"


def _profile_context(profile) -> str:
    return (
        f"Age: {profile.age}\n"
        f"Height: {profile.height_feet} feet\n"
        f"Weight: {profile.weight_lb} lb\n"
        f"Fitness Goal: {profile.fitness_goal}\n"
        f"Activity Level: {profile.activity_level}\n"
        f"Diet Preference: {profile.dietary_preference}"
    )


def _workout_context(recent_workouts) -> str:
    lines = []
    for w in recent_workouts[-14:]:
        groups = ", ".join(w.muscle_groups) or "-"
        lines.append(
            f"- {w.date}: {w.session_type} ({groups}), "
            f"RPE {w.rpe}, {w.duration_min} min"
        )
    return "\n".join(lines)


def generate_response(
        question: str,
        profile=None,
        recent_workouts=None):

    start = time.perf_counter()

    system_prompt = (
        "You are a helpful fitness and nutrition coach. "
        "Provide general, evidence-based advice. "
        "When the user's workout history is provided, use it to "
        "give advice about training frequency and recovery."
    )

    parts = []
    if profile:
        parts.append(f"User Profile:\n{_profile_context(profile)}")
    if recent_workouts:
        parts.append(
            f"Recent Workouts:\n{_workout_context(recent_workouts)}"
        )
    parts.append(f"User Question:\n{question}")
    user_input = "\n\n".join(parts)

    response = client.responses.create(
        model=MODEL,
        instructions=system_prompt,
        input=user_input
    )
    latency = time.perf_counter() - start

    return {
        "answer": response.output_text,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "latency": round(latency, 2)
    }


def generate_coach_message(analysis: dict, fitness_goal: str) -> str:
    prompt = f"""
    The user's fitness goal is: {fitness_goal}

    A rule-based training monitor produced this analysis for today:
    {analysis}

    Write a short coaching message (3-5 sentences) for the user:
    - State clearly whether to strength train today. Do NOT contradict
      the "recommendation" and "should_strength_train" fields.
    - If training, mention the focus muscle groups and intensity, and
      give one practical tip for the session.
    - If not training, explain why in simple terms and say when the next
      strength day is, plus one recovery tip.
    - Be encouraging and specific. No medical advice.
    """

    response = client.responses.create(
        model=MODEL,
        instructions=(
            "You are FitAgent AI, an encouraging strength coach. "
            "Give general fitness guidance, not medical advice."
        ),
        input=prompt
    )
    return response.output_text.strip()
