from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models.context import CaseContext
from app.agents.fact.schema import FactExtractionSchema
from app.agents.fact.prompt import FACT_EXTRACTION_PROMPT
from app.core.config import settings

class FactExtractor(BaseAgent):
    name = "FactExtractor"
    version = "1.0"

    def __init__(self):
        self.llm = self.get_llm(FactExtractionSchema)

    async def run(self, context: CaseContext) -> Dict[str, Any]:
        if not context.scenario:
            return {}

        prompt = FACT_EXTRACTION_PROMPT.format(scenario=context.scenario)
        result: FactExtractionSchema = await self.llm.ainvoke(prompt)
        
        return {
            "facts": result.facts,
            "timeline": result.timeline,
            "entities": result.entities
        }
