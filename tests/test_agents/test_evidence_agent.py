import pytest
from unittest.mock import patch
from app.agents.evidence.agent import EvidenceBuilder
from app.agents.evidence.schema import EvidenceBuilderSchema
from app.models.context import Evidence

@pytest.mark.asyncio
async def test_evidence_builder(mock_context, mock_llm_factory):
    mock_response = EvidenceBuilderSchema(evidence=[Evidence(id='ev1', type='Physical', description='Stolen watch', related_facts=['f1'])])
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(mock_response)):
        agent = EvidenceBuilder()
    result = await agent.run(mock_context)
    assert result['evidence'][0].type == 'Physical'

@pytest.mark.asyncio
async def test_evidence_builder_no_facts(mock_context, mock_llm_factory):
    mock_context.facts = []
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(None)):
        agent = EvidenceBuilder()
    result = await agent.run(mock_context)
    assert result == {}
