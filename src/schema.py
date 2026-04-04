# Response schema definitions for the structured support assistant output.

from pydantic import BaseModel, Field
from typing import  List, Literal, Dict, Annotated

confidence_score = Annotated[float, Field(..., ge= 0.0, le= 1.0)]

class SupportOutput (BaseModel):
    categoty: Literal['billing', 'technical', 'account', 'subscription', 'payment', 'refund', 'login', 'bug', 'feature_request', 'cancellation', 'general']
    priority: Literal['low', 'medium', 'high']
    answer: str
    actions: List[str]
    status: Literal['auto_resolved', 'needs_human_review']
    confidences: Dict[str, confidence_score] = Field(
        ...,
        description = 'Mapa de confianza para cada campo'
    )

class SuportResponse(BaseModel):
    suport_output: SupportOutput
