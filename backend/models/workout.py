from typing import Literal

from pydantic import BaseModel, Field


ExperienceLevel = Literal["Beginner", "Intermediate", "Advanced"]
Equipment = Literal["Full Gym", "Dumbbells Only", "Bodyweight"]
MuscleGroup = Literal["Chest", "Back", "Shoulders", "Arms", "Legs", "Core"]
SessionType = Literal[
    "Strength", "Cardio", "Conditioning", "Mobility", "Rest"
]


class WorkoutPlanRequest(BaseModel):
    fitness_goal: str
    activity_level: str = "Lightly Active"
    days_per_week: int | None = Field(default=None, ge=2, le=6)
    experience: ExperienceLevel = "Beginner"
    equipment: Equipment = "Full Gym"


class Exercise(BaseModel):
    name: str
    sets: int
    reps: str
    rest_sec: int
    notes: str = ""


class WorkoutDay(BaseModel):
    day: str
    session_type: SessionType
    focus: str
    muscle_groups: list[str]
    duration_min: int
    exercises: list[Exercise]


class WorkoutPlan(BaseModel):
    fitness_goal: str
    days_per_week: int
    strength_sessions_per_week: int
    experience: str
    equipment: str
    training_focus: str
    weekly_schedule: list[WorkoutDay]
    tips: list[str]


class WorkoutLogEntry(BaseModel):
    date: str = Field(description="YYYY-MM-DD")
    session_type: SessionType = "Strength"
    muscle_groups: list[MuscleGroup] = []
    rpe: int = Field(default=7, ge=1, le=10)
    duration_min: int = Field(default=45, ge=0, le=600)


class StrengthCheckRequest(BaseModel):
    fitness_goal: str
    activity_level: str = "Lightly Active"
    days_per_week: int | None = Field(default=None, ge=2, le=6)
    workout_log: list[WorkoutLogEntry] = []
    sleep_hours: float = Field(default=7.5, ge=0, le=16)
    soreness: int = Field(default=2, ge=1, le=5)
    energy: int = Field(default=3, ge=1, le=5)
    today: str | None = Field(
        default=None,
        description="User's local date YYYY-MM-DD (defaults to server date)"
    )
    use_ai: bool = True


class MuscleStatus(BaseModel):
    muscle_group: str
    last_trained: str | None
    days_since: int | None
    status: Literal["Recovered", "Recovering"]
    ready_on: str


class StrengthCheckResponse(BaseModel):
    date: str
    recommendation: str
    should_strength_train: bool
    focus: str | None
    focus_muscle_groups: list[str]
    intensity: str | None
    readiness_score: int
    strength_sessions_this_week: int
    weekly_strength_target: int
    days_since_last_strength: int | None
    consecutive_strength_days: int
    next_strength_day: str
    reasons: list[str]
    muscle_status: list[MuscleStatus]
    coach_message: str
    ai_generated: bool
