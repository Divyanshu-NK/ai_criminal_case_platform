import pytest
from unittest.mock import MagicMock
from app.models.context import (
    CaseContext, Fact, Event, Entity, Evidence, Offence, Law, 
    ValidationResult, MissingEvidence, SimilarCase, Strategy, LegalReport
)

@pytest.fixture
def mock_context():
    """Provides a basic CaseContext for tests to mutate."""
    return CaseContext(
        scenario="A stole B's watch at 10 PM.",
        facts=[Fact(id="f1", description="A stole a watch", confidence=0.9)],
        entities=[Entity(id="e1", name="A", role="Accused"), Entity(id="e2", name="B", role="Victim")],
        timeline=[Event(timestamp="10 PM", description="Theft occurred", related_facts=["f1"])]
    )

class MockRunnable:
    def __init__(self, response):
        self.response = response
        
    def invoke(self, *args, **kwargs):
        return self.response
        
    async def ainvoke(self, *args, **kwargs):
        return self.response

@pytest.fixture
def mock_llm_factory():
    """
    Returns a factory function that creates a mocked LLM.
    The mocked LLM's `with_structured_output` will return a runnable 
    that yields the `return_value` passed to the factory.
    """
    def _factory(return_value):
        return MockRunnable(return_value)
    return _factory
