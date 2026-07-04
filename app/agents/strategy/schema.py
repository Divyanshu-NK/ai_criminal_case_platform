from pydantic import BaseModel, Field
from app.models.context import Strategy

class StrategySchema(BaseModel):
    strategy: Strategy = Field(description="Legal strategy including arguments and weaknesses")
