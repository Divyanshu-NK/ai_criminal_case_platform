from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models.context import CaseContext
from app.agents.strategy.schema import StrategySchema
from app.agents.strategy.prompt import STRATEGY_PROMPT
from app.core.config import settings

class StrategyAgent(BaseAgent):
    name = "StrategyAgent"
    version = "1.0"

    def __init__(self):
        self.llm = self.get_llm(StrategySchema)

    async def run(self, context: CaseContext) -> Dict[str, Any]:
        val_str = "\n".join([f"- {sec}: Satisfied? {v.is_satisfied}. Reason: {v.reasoning}" for sec, v in context.validation.items()])
        miss_str = "\n".join([f"- {m.description} (Reason: {m.reason})" for m in context.missing_evidence])
        cases_str = "\n".join([f"- {c.case_name} ({c.year})" for c in context.similar_cases])

        prompt = STRATEGY_PROMPT.format(validation=val_str, missing_evidence=miss_str, similar_cases=cases_str)
        result: StrategySchema = await self.llm.ainvoke(prompt)
        
        return {
            "strategy": result.strategy
        }
