from abc import ABC, abstractmethod
from typing import Dict, Any, Type, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from app.models.context import CaseContext
from app.core.config import settings
from app.core.logging import AgentLoggingCallbackHandler

class BaseAgent(ABC):
    name: str
    version: str

    def get_llm(self, schema: Optional[Type] = None):
        """Returns a configured LLM with the centralized logging callback."""
        llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            temperature=0.0,
            api_key=settings.GEMINI_API_KEY,
            callbacks=[AgentLoggingCallbackHandler(self.name)]
        )
        if schema:
            return llm.with_structured_output(schema)
        return llm

    @abstractmethod
    async def run(self, context: CaseContext) -> Dict[str, Any]:
        """
        Takes the current CaseContext and returns a dictionary of state updates.
        The dictionary keys must match the fields in CaseContext.
        """
        pass
