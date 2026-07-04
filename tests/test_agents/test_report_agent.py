import pytest
from unittest.mock import patch
from app.agents.report.agent import ReportAgent
from app.agents.report.schema import ReportSchema
from app.models.context import LegalReport

@pytest.mark.asyncio
async def test_report_generation(mock_context, mock_llm_factory):
    mock_response = ReportSchema(report=LegalReport(summary='Theft happened', recommended_charges=['BNS 303'], procedural_next_steps=['FIR'], conclusion='Guilty'))
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(mock_response)):
        agent = ReportAgent()
    result = await agent.run(mock_context)
    assert result['report'].summary == 'Theft happened'
