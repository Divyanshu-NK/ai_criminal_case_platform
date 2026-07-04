from typing import Dict, Any
import json
from app.agents.base import BaseAgent
from app.models.context import CaseContext
from app.agents.report.schema import ReportSchema
from app.agents.report.prompt import REPORT_PROMPT
from app.core.config import settings

class ReportAgent(BaseAgent):
    name = "ReportAgent"
    version = "1.0"

    def __init__(self):
        self.llm = self.get_llm(ReportSchema)

    async def run(self, context: CaseContext) -> Dict[str, Any]:
        strat_str = context.strategy.model_dump_json() if context.strategy else "{}"
        
        # Serialize validation dictionary manually
        val_dict = {k: {"is_satisfied": v.is_satisfied, "reasoning": v.reasoning, "missing_ingredients": v.missing_ingredients} for k, v in context.validation.items()}
        val_str = json.dumps(val_dict)

        prompt = REPORT_PROMPT.format(strategy=strat_str, validation=val_str)
        result: ReportSchema = await self.llm.ainvoke(prompt)
        
        return {
            "report": result.report
        }
