import pytest
from unittest.mock import patch
from app.agents.scenario.agent import ScenarioParser
from app.agents.scenario.schema import ScenarioParserSchema

@pytest.mark.asyncio
async def test_scenario_parser(mock_context, mock_llm_factory):
    mock_response = ScenarioParserSchema(cleaned_scenario='Standardized narrative: A committed theft.', jurisdiction='India')
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(mock_response)):
        agent = ScenarioParser()
    result = await agent.run(mock_context)
    assert result['scenario'] == 'Standardized narrative: A committed theft.'

@pytest.mark.asyncio
async def test_scenario_parser_empty(mock_context, mock_llm_factory):
    mock_context.scenario = ''
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(None)):
        agent = ScenarioParser()
    result = await agent.run(mock_context)
    assert result == {}
