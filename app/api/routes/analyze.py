from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.models.context import CaseContext
from app.orchestrator.workflow import create_workflow

router = APIRouter()
workflow = create_workflow()

class AnalyzeRequest(BaseModel):
    scenario: str
    task_type: Optional[str] = "analysis"

@router.post("/analyze", response_model=CaseContext)
async def analyze_case(request: AnalyzeRequest):
    # If a specific task is requested (like Bail Application), we can prefix it to guide the LLM
    final_scenario = request.scenario
    if request.task_type == "charge_sheet":
        final_scenario = f"[TASK: Draft a Charge Sheet based on the following] {request.scenario}"
    elif request.task_type == "bail_application":
        final_scenario = f"[TASK: Draft a Bail Application based on the following] {request.scenario}"
        
    initial_context = CaseContext(scenario=final_scenario)
    state = {"context": initial_context}
    
    try:
        result = await workflow.ainvoke(state)
        return result["context"]
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
