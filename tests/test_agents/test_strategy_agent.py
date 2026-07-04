import pytest
from unittest.mock import patch
from app.agents.strategy.agent import StrategyAgent
from app.agents.strategy.schema import StrategySchema
from app.models.context import Strategy

@pytest.mark.asyncio
async def test_defense_strategy(mock_context, mock_llm_factory):
    mock_response = StrategySchema(strategy=Strategy(prosecution_arguments=['A took it'], defense_arguments=['B gave it'], key_weaknesses=['No CCTV']))
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(mock_response)):
        agent = StrategyAgent()
    result = await agent.run(mock_context)
    assert result['strategy'].key_weaknesses[0] == 'No CCTV'
