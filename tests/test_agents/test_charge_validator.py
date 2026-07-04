import pytest
from unittest.mock import patch
from app.agents.charge_validator.agent import ChargeValidator
from app.agents.charge_validator.schema import ChargeValidatorSchema
from app.models.context import ValidationResult, MissingEvidence, Law, Offence

@pytest.mark.asyncio
async def test_charge_validator(mock_context, mock_llm_factory):
    mock_context.laws = [Law(act_name='BNS', section='303', text='Theft', ingredients=['Taking', 'Movable'])]
    mock_context.offences = [Offence(id='o1', name='Theft', description='Theft', potential_sections=['BNS 303'])]
    mock_response = ChargeValidatorSchema(validation={'BNS 303': ValidationResult(is_satisfied=False, reasoning='Missing intent', missing_ingredients=['Intent'])}, missing_evidence=[MissingEvidence(description='CCTV', reason='To prove intent')])
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(mock_response)):
        agent = ChargeValidator()
    result = await agent.run(mock_context)
    assert result['validation']['BNS 303'].is_satisfied is False

@pytest.mark.asyncio
async def test_charge_validator_no_laws(mock_context, mock_llm_factory):
    mock_context.laws = []
    with patch('app.agents.base.BaseAgent.get_llm', return_value=mock_llm_factory(None)):
        agent = ChargeValidator()
    result = await agent.run(mock_context)
    assert result == {}
