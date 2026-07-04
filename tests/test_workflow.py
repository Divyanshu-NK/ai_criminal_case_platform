import pytest
from unittest.mock import patch, AsyncMock
from app.orchestrator.workflow import create_workflow, GraphState
from app.models.context import CaseContext

@pytest.mark.asyncio
async def test_workflow_execution():
    workflow = create_workflow()
    
    # We mock out the run method of every agent to simply return empty dicts or specific updates
    with patch("app.agents.scenario.agent.ScenarioParser.run", new_callable=AsyncMock) as mock_scenario, \
         patch("app.agents.fact.agent.FactExtractor.run", new_callable=AsyncMock) as mock_fact, \
         patch("app.agents.evidence.agent.EvidenceBuilder.run", new_callable=AsyncMock) as mock_evidence, \
         patch("app.agents.offence.agent.OffenceDiscovery.run", new_callable=AsyncMock) as mock_offence, \
         patch("app.agents.law_retrieval.agent.LawRetriever.run", new_callable=AsyncMock) as mock_law, \
         patch("app.agents.charge_validator.agent.ChargeValidator.run", new_callable=AsyncMock) as mock_validator, \
         patch("app.agents.case_retrieval.agent.CaseRetriever.run", new_callable=AsyncMock) as mock_case, \
         patch("app.agents.strategy.agent.StrategyAgent.run", new_callable=AsyncMock) as mock_strategy, \
         patch("app.agents.procedure.agent.ProcedureAgent.run", new_callable=AsyncMock) as mock_procedure, \
         patch("app.agents.report.agent.ReportAgent.run", new_callable=AsyncMock) as mock_report:
             
        # Just setting one of them to return an update
        mock_scenario.return_value = {"scenario": "Tested scenario"}
        mock_fact.return_value = {}
        mock_evidence.return_value = {}
        mock_offence.return_value = {}
        mock_law.return_value = {}
        mock_validator.return_value = {}
        mock_case.return_value = {}
        mock_strategy.return_value = {}
        mock_procedure.return_value = {}
        mock_report.return_value = {}
        
        context = CaseContext(scenario="Initial")
        state: GraphState = {"context": context}
        
        result = await workflow.ainvoke(state)
        
        assert "context" in result
        assert result["context"].scenario == "Tested scenario"
        
        # Verify that all nodes were visited
        mock_scenario.assert_called_once()
        mock_fact.assert_called_once()
        mock_evidence.assert_called_once()
        mock_offence.assert_called_once()
        mock_law.assert_called_once()
        mock_validator.assert_called_once()
        mock_case.assert_called_once()
        mock_strategy.assert_called_once()
        mock_procedure.assert_called_once()
        mock_report.assert_called_once()
