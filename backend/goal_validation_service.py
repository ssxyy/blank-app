
from pydantic import BaseModel, Field


class WeightLossAssessment(BaseModel):
    total_loss_lb: float
    weekly_loss_lb: float
    needs_review: bool
    message: str


def assess_weight_loss_goal(
    current_weight_lb: float,
    target_weight_lb: float,
    timeline_weeks: int
) -> WeightLossAssessment:

    if current_weight_lb <= 0:
        raise ValueError("Current weight must be positive")

    if target_weight_lb <= 0:
        raise ValueError("Target weight must be positive")

    if timeline_weeks <= 0:
        raise ValueError("Timeline must be positive")

    if target_weight_lb >= current_weight_lb:
        raise ValueError(
            "Target weight must be below current weight"
        )

    total_loss = current_weight_lb - target_weight_lb
    weekly_loss = total_loss / timeline_weeks

    needs_review = weekly_loss > 2.0

    if needs_review:
        message = (
            "Your requested weight-loss rate is relatively fast. "
            "Consider a longer timeline and seek individualized "
            "guidance before following a restrictive plan."
        )
    else:
        message = (
            "The requested weekly rate is within a commonly "
            "discussed gradual weight-loss range. This does not "
            "confirm that the target weight is appropriate."
        )

    return WeightLossAssessment(
        total_loss_lb=round(total_loss, 2),
        weekly_loss_lb=round(weekly_loss, 2),
        needs_review=needs_review,
        message=message
    )
