from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import dotenv
from app.api.routes import analyze, system
import os

dotenv.load_dotenv()

app = FastAPI(title="AI Criminal Case Platform API")

# API Routes
app.include_router(analyze.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(system.router, tags=["System"])

# Ensure static directory exists
os.makedirs("static", exist_ok=True)

# Mount static files for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the index.html at the root URL
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")
