from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models.context import CaseContext
from app.agents.offence.schema import OffenceDiscoverySchema
from app.agents.offence.prompt import OFFENCE_DISCOVERY_PROMPT
from app.core.config import settings

class OffenceDiscovery(BaseAgent):
    name = "OffenceDiscovery"
    version = "1.0"

    def __init__(self):
        self.llm = self.get_llm(OffenceDiscoverySchema)

    async def run(self, context: CaseContext) -> Dict[str, Any]:
        if not context.facts:
            return {}
            
        facts_str = "\n".join([f"- {f.description}" for f in context.facts])
        timeline_str = "\n".join([f"- {e.timestamp}: {e.description}" for e in context.timeline])

        prompt = OFFENCE_DISCOVERY_PROMPT.format(facts=facts_str, timeline=timeline_str)
        result: OffenceDiscoverySchema = await self.llm.ainvoke(prompt)
        
        return {
            "offences": result.offences
        }
