from pydantic import BaseModel, Field
from typing import Dict, List
from app.models.context import ValidationResult, MissingEvidence

class ChargeValidatorSchema(BaseModel):
    validation: Dict[str, ValidationResult] = Field(description="Mapping of Section string (e.g. '103') to ValidationResult")
    missing_evidence: List[MissingEvidence] = Field(description="What evidence is missing to fulfill ingredients")
