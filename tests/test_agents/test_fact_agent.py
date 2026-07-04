import pytest
from unittest.mock import patch
from app.agents.fact.agent import FactExtractor
from app.agents.fact.schema import FactExtractionSchema
from app.models.context import Fact, Entity, Event

@pytest.mark.asyncio
async def test_fact_extractor(mock_context, mock_llm_factory):
    mock_response = FactExtractionSchema(
        facts=[Fact(id='f2', description='A new fact', confidence=0.8)],
        entities=[Entity(id='e3', name='C', role='Witness')],
        timeline=[Event(timestamp='11 PM', description='Witness saw something', related_facts=['f2'])]
    )
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(mock_response)):
        agent = FactExtractor()
    result = await agent.run(mock_context)
    assert 'facts' in result
    assert result['facts'][0].id == 'f2'

@pytest.mark.asyncio
async def test_fact_extractor_empty_scenario(mock_context, mock_llm_factory):
    mock_context.scenario = ''
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(None)):
        agent = FactExtractor()
    result = await agent.run(mock_context)
    assert result == {}
