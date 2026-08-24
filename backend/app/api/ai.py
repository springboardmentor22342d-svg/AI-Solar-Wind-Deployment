from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()


class AIRequest(BaseModel):

    question: str
    analysis: dict


@router.post("/ask")
def ask_ai(request: AIRequest):

    question = request.question.lower()

    analysis = request.analysis

    solar = analysis.get("solar", 0)
    wind = analysis.get("wind", 0)
    suitability = analysis.get(
        "suitability",
        0
    )

    category = analysis.get(
        "category",
        "Unknown"
    )


    # ------------------------------------------------------
    # SIMPLE AI-LIKE SITE ASSISTANT
    # ------------------------------------------------------

    if "solar" in question:

        answer = (
            f"The analyzed site has an average "
            f"solar irradiance of {solar} W/m². "
            f"This value can be used to estimate "
            f"solar energy generation potential."
        )

    elif "wind" in question:

        answer = (
            f"The analyzed site has an average "
            f"wind speed of {wind} m/s. "
            f"The wind resource should be considered "
            f"along with the site's wind capacity factor."
        )

    elif (
        "suitable" in question
        or "suitability" in question
    ):

        answer = (
            f"The site's current suitability score "
            f"is {suitability}%, classified as "
            f"{category}."
        )

    elif "energy" in question:

        answer = (
            "The site can be evaluated using its "
            "solar generation, wind generation and "
            "combined hybrid energy prediction."
        )

    else:

        answer = (
            f"The analyzed location has a "
            f"suitability score of {suitability}%. "
            f"Solar irradiance is {solar} W/m² and "
            f"wind speed is {wind} m/s."
        )


    return {
        "answer": answer
    }