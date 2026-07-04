from typing import Dict, Any
from app.agents.base import BaseAgent
from app.models.context import CaseContext
from app.rag.retrieval import CaseRetrieverService

class CaseRetriever(BaseAgent):
    name = "CaseRetriever"
    version = "1.0"

    def __init__(self):
        self.retriever = CaseRetrieverService()

    async def run(self, context: CaseContext) -> Dict[str, Any]:
        if not context.offences:
            return {}
            
        search_terms = [off.name for off in context.offences]
        cases = self.retriever.retrieve_cases(search_terms)
        
        return {
            "similar_cases": cases
        }
