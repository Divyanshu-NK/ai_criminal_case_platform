from pydantic import BaseModel, Field
from typing import List
from app.models.context import Evidence

class EvidenceBuilderSchema(BaseModel):
    evidence: List[Evidence] = Field(description="Extracted or inferred evidence based on facts")
