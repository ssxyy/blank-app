from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field
from openai import OpenAIError
from backend.llm_service import generate_response
from backend.nutrition_service import generate_meal_plan
from backend.models.meal_plan import MealPlan
from backend.goal_validation_service import(assess_weight_loss_goal,WeightLossAssessment)

app=FastAPI(title="FitAgent AI Backend")

class UserProfile(BaseModel):
    age:int= Field(ge=18,le=100)
    height_feet:float=Field(gt=0.0)
    weight_lb:float=Field(gt=0)
    fitness_goal:str
    activity_level: str
    dietary_preference: str

    target_weight_lb: float | None = None
    timeline_weeks: int | None = None

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    profile: UserProfile | None = None

class ChatResponse(BaseModel):
    answer: str
    input_tokens:int
    output_tokens:int
    latency:float

class WeightLossGoalRequest(BaseModel):
    current_weight_lb: float = Field(gt=0)
    target_weight_lb: float = Field(gt=0)
    timeline_weeks: int = Field(ge=1, le=104)



@app.get("/health")
def health_check():
    return {"status": "up"}

@app.post("/api/v1/fitness/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
      return generate_response(request.question,request.profile)
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
    if profile.fitness_goal == "Weight Loss":

        if (
            profile.target_weight_lb is None
            or profile.timeline_weeks is None
        ):
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
            raise HTTPException(
                status_code=422,
                detail=str(e)
            )

        if assessment.needs_review:
            raise HTTPException(
                status_code=422,
                detail=assessment.message
            )
    try:
        return generate_meal_plan(profile.model_dump())
    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="Failed to generate meal plan"
        )



@app.post(
    "/api/v1/fitness/assess-goal",
    response_model = WeightLossAssessment
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


    
