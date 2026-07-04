from pydantic import BaseModel, Field
from app.models.context import LegalReport

class ReportSchema(BaseModel):
    report: LegalReport = Field(description="Final legal report summarizing the entire case analysis")
