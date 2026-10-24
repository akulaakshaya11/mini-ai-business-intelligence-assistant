
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.analytics import (
    total_revenue,
    top_product,
    monthly_revenue_trend,
    top_region,
    compare_months,
)
from app.interpreter import interpret_question

app = FastAPI(
    title="Mini AI Business Intelligence Assistant",
    description=(
        "Ask natural-language questions about sales data "
        "and receive answers backed by SQL queries."
    ),
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=500,
        description="A business question about sales data",
    )


@app.get("/")
def home():
    return {
        "message": "Mini AI Business Intelligence Assistant",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a business question.",
        )

    # Step 1: Use Gemini to classify the question.
    try:
        interpretation = interpret_question(question)
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "The AI service could not interpret the question. "
                "Check your API key, model availability, and quota."
            ),
        ) from exc

    intent = interpretation["intent"]

    # Step 2: Execute only approved analytics functions.
    try:
        if intent == "total_revenue":
            answer = {
                "total_revenue": total_revenue()
            }

        elif intent == "top_product":
            answer = {
                "top_product": top_product()
            }

        elif intent == "monthly_revenue_trend":
            answer = {
                "monthly_revenue": monthly_revenue_trend()
            }

        elif intent == "top_region":
            answer = {
                "top_region": top_region()
            }

        elif intent == "compare_months":
            answer = {
                "month_comparison": compare_months(
                    interpretation["month_a"],
                    interpretation["month_b"],
                )
            }

        elif intent == "unsupported":
            raise HTTPException(
                status_code=400,
                detail=(
                    "I can answer questions about total revenue, "
                    "top product, monthly revenue trends, top region, "
                    "and comparisons between two months."
                ),
            )

        else:
            raise HTTPException(
                status_code=400,
                detail="The AI returned an unrecognized intent.",
            )

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to calculate the answer from the database.",
        ) from exc

    # Step 3: Return the SQL-backed answer.
    return {
        "question": question,
        "interpreted_intent": intent,
        "answer": answer,
    }
