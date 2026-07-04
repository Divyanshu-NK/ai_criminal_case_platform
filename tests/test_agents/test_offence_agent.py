import pytest
from unittest.mock import patch
from app.agents.offence.agent import OffenceDiscovery
from app.agents.offence.schema import OffenceDiscoverySchema
from app.models.context import Offence

@pytest.mark.asyncio
async def test_offence_discovery(mock_context, mock_llm_factory):
    mock_response = OffenceDiscoverySchema(offences=[Offence(id='o1', name='Theft', description='Taking property', potential_sections=['BNS 303'])])
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(mock_response)):
        agent = OffenceDiscovery()
    result = await agent.run(mock_context)
    assert result['offences'][0].name == 'Theft'

@pytest.mark.asyncio
async def test_offence_discovery_no_facts(mock_context, mock_llm_factory):
    mock_context.facts = []
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(None)):
        agent = OffenceDiscovery()
    result = await agent.run(mock_context)
    assert result == {}
