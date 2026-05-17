# Response schema definitions for the structured support assistant output.

from pydantic import BaseModel, Field
from typing import  List, Literal, Annotated

class SupportOutput (BaseModel):
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
