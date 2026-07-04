import pytest
from unittest.mock import patch
from app.agents.procedure.agent import ProcedureAgent
from app.agents.procedure.schema import ProcedureSchema
from app.models.context import ValidationResult, Offence

@pytest.mark.asyncio
async def test_procedural_guidance(mock_context, mock_llm_factory):
    mock_context.validation = {'BNS 303': ValidationResult(is_satisfied=True, reasoning='All good')}
    mock_context.offences = [Offence(id='o1', name='Theft', description='Theft', potential_sections=['BNS 303'])]
    mock_response = ProcedureSchema(procedural_steps=['File FIR', 'Collect evidence'])
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(mock_response)):
        agent = ProcedureAgent()
    result = await agent.run(mock_context)
    assert result['procedural_steps'][0] == 'File FIR'

@pytest.mark.asyncio
async def test_procedural_guidance_no_validation(mock_context, mock_llm_factory):
    mock_context.validation = {}
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(None)):
        agent = ProcedureAgent()
    result = await agent.run(mock_context)
    assert result == {}
