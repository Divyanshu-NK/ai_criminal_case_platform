from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from app.models.context import CaseContext
from app.agents.scenario.agent import ScenarioParser
from app.agents.fact.agent import FactExtractor
from app.agents.evidence.agent import EvidenceBuilder
from app.agents.offence.agent import OffenceDiscovery
from app.agents.law_retrieval.agent import LawRetriever
from app.agents.charge_validator.agent import ChargeValidator
from app.agents.case_retrieval.agent import CaseRetriever
from app.agents.strategy.agent import StrategyAgent
from app.agents.procedure.agent import ProcedureAgent
from app.agents.report.agent import ReportAgent

class GraphState(TypedDict):
    context: CaseContext

async def scenario_node(state: GraphState):
    agent = ScenarioParser()
    updates = await agent.run(state["context"])
    for k, v in updates.items():
        setattr(state["context"], k, v)
    return {"context": state["context"]}

async def fact_node(state: GraphState):
    agent = FactExtractor()
    updates = await agent.run(state["context"])
    for k, v in updates.items():
        setattr(state["context"], k, v)
    return {"context": state["context"]}

async def evidence_node(state: GraphState):
    agent = EvidenceBuilder()
    updates = await agent.run(state["context"])
    for k, v in updates.items():
        setattr(state["context"], k, v)
    return {"context": state["context"]}

async def offence_node(state: GraphState):
    agent = OffenceDiscovery()
    updates = await agent.run(state["context"])
    for k, v in updates.items():
        setattr(state["context"], k, v)
    return {"context": state["context"]}

async def law_node(state: GraphState):
    agent = LawRetriever()
    updates = await agent.run(state["context"])
    for k, v in updates.items():
        setattr(state["context"], k, v)
    return {"context": state["context"]}

async def validator_node(state: GraphState):
    agent = ChargeValidator()
    updates = await agent.run(state["context"])
    for k, v in updates.items():
        setattr(state["context"], k, v)
    return {"context": state["context"]}

async def case_node(state: GraphState):
    agent = CaseRetriever()
    updates = await agent.run(state["context"])
    for k, v in updates.items():
        setattr(state["context"], k, v)
    return {"context": state["context"]}

async def strategy_node(state: GraphState):
    agent = StrategyAgent()
    updates = await agent.run(state["context"])
    for k, v in updates.items():
        setattr(state["context"], k, v)
    return {"context": state["context"]}

async def procedure_node(state: GraphState):
    agent = ProcedureAgent()
    updates = await agent.run(state["context"])
    for k, v in updates.items():
        setattr(state["context"], k, v)
    return {"context": state["context"]}

async def report_node(state: GraphState):
    agent = ReportAgent()
    updates = await agent.run(state["context"])
    for k, v in updates.items():
        setattr(state["context"], k, v)
    return {"context": state["context"]}

def create_workflow():
    workflow = StateGraph(GraphState)
    
    workflow.add_node("scenario_parser", scenario_node)
    workflow.add_node("fact_extractor", fact_node)
    workflow.add_node("evidence_builder", evidence_node)
    workflow.add_node("offence_discovery", offence_node)
    workflow.add_node("law_retriever", law_node)
    workflow.add_node("charge_validator", validator_node)
    workflow.add_node("case_retriever", case_node)
    workflow.add_node("strategy_agent", strategy_node)
    workflow.add_node("procedure_agent", procedure_node)
    workflow.add_node("report_agent", report_node)
    
    # Linear edges
    workflow.add_edge(START, "scenario_parser")
    workflow.add_edge("scenario_parser", "fact_extractor")
    workflow.add_edge("fact_extractor", "evidence_builder")
    workflow.add_edge("evidence_builder", "offence_discovery")
    workflow.add_edge("offence_discovery", "law_retriever")
    workflow.add_edge("law_retriever", "charge_validator")
    workflow.add_edge("charge_validator", "case_retriever")
    workflow.add_edge("case_retriever", "strategy_agent")
    workflow.add_edge("strategy_agent", "procedure_agent")
    workflow.add_edge("procedure_agent", "report_agent")
    workflow.add_edge("report_agent", END)
    
    return workflow.compile()
