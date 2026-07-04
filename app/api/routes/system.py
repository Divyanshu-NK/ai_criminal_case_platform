from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.post("/admin/reindex")
def admin_reindex():
    # Placeholder for RAG reindexing endpoint
    return {"status": "reindexed"}

@router.get("/metrics")
def metrics():
    # Placeholder for metrics
    return {"status": "ok"}
