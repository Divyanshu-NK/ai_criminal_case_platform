from pydantic import BaseModel, Field
from typing import List

class ProcedureSchema(BaseModel):
    procedural_steps: List[str] = Field(..., description="A list of required procedural next steps based on BNSS or BSA.")
