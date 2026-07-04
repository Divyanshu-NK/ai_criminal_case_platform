from fastapi import FastAPI
import dotenv
from app.api.routes import analyze, system

dotenv.load_dotenv()

app = FastAPI(title="AI Criminal Case Platform API")

app.include_router(analyze.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(system.router, tags=["System"])
