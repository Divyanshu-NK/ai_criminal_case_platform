from pydantic import BaseModel, Field

class ScenarioParserSchema(BaseModel):
    cleaned_scenario: str = Field(..., description="The cleaned and standardized narrative of the scenario.")
    jurisdiction: str = Field(..., description="The identified jurisdiction, e.g., India.")
