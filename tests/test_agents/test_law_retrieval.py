import pytest
from unittest.mock import patch
from app.agents.law_retrieval.agent import LawRetriever
from app.models.context import Law, Offence

@pytest.mark.asyncio
async def test_law_retriever(mock_context):
    mock_context.offences = [Offence(id='o1', name='Theft', description='Theft', potential_sections=['BNS 303'])]
    mock_laws = [Law(act_name='BNS', section='303', text='Punishment for theft')]
    with patch('app.agents.law_retrieval.agent.LawRetrieverService.retrieve_laws', return_value=mock_laws):
        agent = LawRetriever()
        result = await agent.run(mock_context)
    assert result['laws'][0].section == '303'

@pytest.mark.asyncio
async def test_law_retriever_no_offences(mock_context):
    mock_context.offences = []
    agent = LawRetriever()
    result = await agent.run(mock_context)
    assert result == {}
