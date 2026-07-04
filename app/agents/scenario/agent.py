from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models.context import CaseContext
from app.agents.scenario.schema import ScenarioParserSchema
from app.agents.scenario.prompt import SCENARIO_PARSER_PROMPT
from app.core.config import settings

class ScenarioParser(BaseAgent):
    name = "ScenarioParser"
    version = "1.0"

    def __init__(self):
        self.llm = self.get_llm(ScenarioParserSchema)

    async def run(self, context: CaseContext) -> Dict[str, Any]:
        if not context.scenario:
            return {}

        prompt = SCENARIO_PARSER_PROMPT.format(scenario=context.scenario)
        result: ScenarioParserSchema = await self.llm.ainvoke(prompt)
        
        return {
            "scenario": result.cleaned_scenario
        }
