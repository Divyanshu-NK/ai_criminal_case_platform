from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models.context import CaseContext
from app.agents.procedure.schema import ProcedureSchema
from app.agents.procedure.prompt import PROCEDURE_PROMPT
from app.core.config import settings

class ProcedureAgent(BaseAgent):
    name = "ProcedureAgent"
    version = "1.0"

    def __init__(self):
        self.llm = self.get_llm(ProcedureSchema)

    async def run(self, context: CaseContext) -> Dict[str, Any]:
        if not context.offences:
            return {}

        offences_str = "\n".join([f"[{o.id}] {o.name}" for o in context.offences])
        prompt = PROCEDURE_PROMPT.format(offences=offences_str)
        
        result: ProcedureSchema = await self.llm.ainvoke(prompt)
        
        return {
            "procedural_steps": result.procedural_steps
        }
