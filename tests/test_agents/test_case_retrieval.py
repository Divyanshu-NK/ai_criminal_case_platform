import pytest
from unittest.mock import patch
from app.agents.case_retrieval.agent import CaseRetriever
from app.models.context import SimilarCase, Offence

@pytest.mark.asyncio
async def test_case_retriever(mock_context):
    mock_context.offences = [Offence(id='o1', name='Theft', description='Theft', potential_sections=['BNS 303'])]
    mock_cases = [SimilarCase(case_name='State vs A', court='Supreme Court', year=2023, summary='Theft case', relevance='High')]
    with patch('app.agents.case_retrieval.agent.CaseRetrieverService.retrieve_cases', return_value=mock_cases):
        agent = CaseRetriever()
        result = await agent.run(mock_context)
    assert result['similar_cases'][0].case_name == 'State vs A'

@pytest.mark.asyncio
async def test_case_retriever_no_offences(mock_context):
    mock_context.offences = []
    agent = CaseRetriever()
    result = await agent.run(mock_context)
    assert result == {}
