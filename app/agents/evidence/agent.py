from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models.context import CaseContext
from app.agents.evidence.schema import EvidenceBuilderSchema
from app.agents.evidence.prompt import EVIDENCE_BUILDER_PROMPT
from app.core.config import settings

class EvidenceBuilder(BaseAgent):
    name = "EvidenceBuilder"
    version = "1.0"

    def __init__(self):
        self.llm = self.get_llm(EvidenceBuilderSchema)

    async def run(self, context: CaseContext) -> Dict[str, Any]:
        if not context.facts:
            return {}
            
        facts_str = "\n".join([f"[{f.id}] {f.description}" for f in context.facts])

        prompt = EVIDENCE_BUILDER_PROMPT.format(facts=facts_str)
        result: EvidenceBuilderSchema = await self.llm.ainvoke(prompt)
        
        return {
            "evidence": result.evidence
        }
