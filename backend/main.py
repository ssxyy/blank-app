from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAIError

from backend.llm_service import generate_response, generate_coach_message
from backend.nutrition_service import (
    generate_meal_plan,
    generate_multi_day_meal_plan,
)
from backend.models.meal_plan import MealPlan, MultiDayMealPlan
from backend.models.workout import (
    WorkoutPlanRequest,
    WorkoutPlan,
    WorkoutLogEntry,
    StrengthCheckRequest,
    StrengthCheckResponse,
)
from backend.goal_validation_service import (
    assess_weight_loss_goal,
    WeightLossAssessment,
)
from backend.workout_service import (
    generate_workout_plan,
    default_days_per_week,
)
from backend.strength_coach import (
    analyze_strength_readiness,
    fallback_coach_message,
)

app = FastAPI(title="FitAgent AI Backend")


class UserProfile(BaseModel):
    age: int = Field(ge=18, le=100)
    height_feet: float = Field(gt=0.0)
    weight_lb: float = Field(gt=0)
    fitness_goal: str
    activity_level: str
    dietary_preference: str

    target_weight_lb: float | None = None
    timeline_weeks: int | None = None


class MultiDayMealPlanRequest(UserProfile):
    days: Literal[3, 7] = 7


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    profile: UserProfile | None = None
    recent_workouts: list[WorkoutLogEntry] | None = None


class ChatResponse(BaseModel):
    answer: str
    input_tokens: int
    output_tokens: int
    latency: float


class WeightLossGoalRequest(BaseModel):
    current_weight_lb: float = Field(gt=0)
    target_weight_lb: float = Field(gt=0)
    timeline_weeks: int = Field(ge=1, le=104)


def _validate_weight_loss_goal(profile: UserProfile) -> None:
    if profile.fitness_goal != "Weight Loss":
        return

    if profile.target_weight_lb is None or profile.timeline_weeks is None:
        raise HTTPException(
            status_code=422,
            detail="Weight Loss requires target weight and timeline"
        )

    try:
        assessment = assess_weight_loss_goal(
            current_weight_lb=profile.weight_lb,
            target_weight_lb=profile.target_weight_lb,
            timeline_weeks=profile.timeline_weeks
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    if assessment.needs_review:
        raise HTTPException(status_code=422, detail=assessment.message)


@app.get("/health")
def health_check():
    return {"status": "up"}


@app.post("/api/v1/fitness/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return generate_response(
            request.question,
            request.profile,
            request.recent_workouts
        )
    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="LLM Service unavailable"
        )


@app.post(
    "/api/v1/nutrition/meal-plan",
    response_model=MealPlan
)
def create_meal_plan(profile: UserProfile):
    _validate_weight_loss_goal(profile)
    try:
        return generate_meal_plan(profile.model_dump())
    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="Failed to generate meal plan"
        )


@app.post(
    "/api/v1/nutrition/meal-plan/multi-day",
    response_model=MultiDayMealPlan
)
def create_multi_day_meal_plan(request: MultiDayMealPlanRequest):
    _validate_weight_loss_goal(request)
    profile = request.model_dump(exclude={"days"})
    try:
        return generate_multi_day_meal_plan(profile, request.days)
    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="Failed to generate meal plan"
        )
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))


@app.post(
    "/api/v1/workout/plan",
    response_model=WorkoutPlan
)
def create_workout_plan(request: WorkoutPlanRequest):
    return generate_workout_plan(
        fitness_goal=request.fitness_goal,
        days_per_week=request.days_per_week,
        activity_level=request.activity_level,
        experience=request.experience,
        equipment=request.equipment,
    )


@app.post(
    "/api/v1/coach/strength-check",
    response_model=StrengthCheckResponse
)
def strength_check(request: StrengthCheckRequest):
    days_per_week = request.days_per_week
    if days_per_week is None:
        days_per_week = default_days_per_week(request.activity_level)

    try:
        analysis = analyze_strength_readiness(
            workout_log=[e.model_dump() for e in request.workout_log],
            fitness_goal=request.fitness_goal,
            days_per_week=days_per_week,
            sleep_hours=request.sleep_hours,
            soreness=request.soreness,
            energy=request.energy,
            today=request.today,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    coach_message = None
    ai_generated = False
    if request.use_ai:
        try:
            coach_message = generate_coach_message(
                analysis, request.fitness_goal
            )
            ai_generated = True
        except OpenAIError:
            coach_message = None

    if not coach_message:
        coach_message = fallback_coach_message(analysis)
        ai_generated = False

    return {
        **analysis,
        "coach_message": coach_message,
        "ai_generated": ai_generated,
    }


@app.post(
    "/api/v1/fitness/assess-goal",
    response_model=WeightLossAssessment
)
def access_goal(request: WeightLossGoalRequest):
    try:
        return assess_weight_loss_goal(
            current_weight_lb=request.current_weight_lb,
            target_weight_lb=request.target_weight_lb,
            timeline_weeks=request.timeline_weeks
        )
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
