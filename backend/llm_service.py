from openai import OpenAI
import time
from pydantic import BaseModel

client = OpenAI()

class UserProfileContext(BaseModel):
    age:int
    height_feet:float
    weight_lb:float
    fitness_goal:str
    activity_leval:str
    dietary_preference:str



def generate_response(
        question: str,
        profile: UserProfileContext | None = None):
    
    start = time.perf_counter()

    system_prompt=(

         "You are a helpful fitness and nutrition coach."
          "Provide general,evidence-based advice."

    )

    user_input=question

    if profile:
        profile_context = (
            f"Age: {profile.age}\n"
            f"Height: {profile.height_feet} feet\n"
            f"Weight: {profile.weight_lb} lb\n"
            f"Fitness Goal: {profile.fitness_goal}\n"
            f"Activity Level: {profile.activity_level}\n"
            f"Diet Preference: {profile.dietary_preference}"
        )
        user_input = (
            f"User Profile:\n{profile_context}\n\n"
            f"User Question:\n{question}"
        )

    response=client.responses.create(
        model="gpt-4.1-mini",
        instructions=system_prompt,
        input=user_input
    )
    latency = time.perf_counter()-start

    return{
        "answer":response.output_text,
        "input_tokens":response.usage.input_tokens,
        "output_tokens":response.usage.output_tokens,
        "latency":round(latency,2)
    }