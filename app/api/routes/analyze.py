from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.context import CaseContext
from app.orchestrator.workflow import create_workflow

router = APIRouter()
workflow = create_workflow()

class AnalyzeRequest(BaseModel):
    scenario: str

@router.post("/analyze", response_model=CaseContext)
async def analyze_case(request: AnalyzeRequest):
    initial_context = CaseContext(scenario=request.scenario)
    state = {"context": initial_context}
    
    try:
        result = await workflow.ainvoke(state)
        return result["context"]
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
