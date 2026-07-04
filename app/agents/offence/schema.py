from pydantic import BaseModel, Field
from typing import List
from app.models.context import Offence

class OffenceDiscoverySchema(BaseModel):
    offences: List[Offence] = Field(description="List of possible offences discovered from facts and evidence")
