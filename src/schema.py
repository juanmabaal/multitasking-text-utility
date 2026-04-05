# Response schema definitions for the structured support assistant output.

from pydantic import BaseModel, Field
from typing import  List, Literal, Annotated

confidence_score = Annotated[float, Field(..., ge= 0.0, le= 1.0)]

class FieldConfidences(BaseModel):
    category: confidence_score
    priority: confidence_score
    answer: confidence_score
    actions: confidence_score
    status: confidence_score

class SupportOutput (BaseModel):
    confidences: FieldConfidences  = Field(
        ...,
        description = 'Mapa de confianza para cada campo'
    )
    category: Literal[
        "billing",
        "technical",
        "account",
        "subscription",
        "payment",
        "refund",
        "login",
        "bug",
        "feature_request",
        "cancellation",
        "general",
    ]
    priority: Literal["low", "medium", "high"]
    answer: str
    actions: List[str]
    status: Literal["auto_resolved", "needs_human_review"]
    
class SupportResponse(BaseModel):
    support_output: SupportOutput
