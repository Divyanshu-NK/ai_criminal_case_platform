from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models.context import CaseContext
from app.agents.charge_validator.schema import ChargeValidatorSchema
from app.agents.charge_validator.prompt import CHARGE_VALIDATOR_PROMPT
from app.core.config import settings

class ChargeValidator(BaseAgent):
    name = "ChargeValidator"
    version = "1.0"

    def __init__(self):
        self.llm = self.get_llm(ChargeValidatorSchema)

    async def run(self, context: CaseContext) -> Dict[str, Any]:
        if not context.laws or not context.facts:
            return {}
            
        laws_str = "\n".join([f"- {l.act_name} {l.section}: Ingredients: {', '.join(l.ingredients)}" for l in context.laws])
        facts_str = "\n".join([f"- {f.description}" for f in context.facts])
        ev_str = "\n".join([f"- {e.description} ({e.type})" for e in context.evidence])

        prompt = CHARGE_VALIDATOR_PROMPT.format(laws=laws_str, facts=facts_str, evidence=ev_str)
        result: ChargeValidatorSchema = await self.llm.ainvoke(prompt)
        
        return {
            "validation": result.validation,
            "missing_evidence": result.missing_evidence
        }
