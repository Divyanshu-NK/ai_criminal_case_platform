from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models.context import CaseContext
from app.rag.retrieval import LawRetrieverService

class LawRetriever(BaseAgent):
    name = "LawRetriever"
    version = "1.0"

    def __init__(self):
        self.retriever = LawRetrieverService()

    async def run(self, context: CaseContext) -> Dict[str, Any]:
        if not context.offences:
            return {}
            
        sections_to_lookup = []
        for off in context.offences:
            sections_to_lookup.extend(off.potential_sections)
            sections_to_lookup.append(off.name)
            
        laws = self.retriever.retrieve_laws(sections_to_lookup)
        
        # Deduplicate laws
        unique_laws = {f"{law.act_name}_{law.section}": law for law in laws}
        
        return {
            "laws": list(unique_laws.values())
        }
