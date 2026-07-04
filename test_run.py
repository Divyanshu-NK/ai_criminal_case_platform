import asyncio
import json
import sys
from app.api.routes.analyze import analyze_case, AnalyzeRequest

async def run():
    scenario = "Ramesh and Suresh were arguing over a land dispute. Ramesh took a stick and struck Suresh on the head, causing him to bleed. Suresh filed a complaint at the local police station."
    req = AnalyzeRequest(scenario=scenario)
    
    print("Running analysis pipeline...")
    try:
        result = await analyze_case(req)
        print("\n--- Pipeline Completed ---")
        print(result.model_dump_json(indent=2))
    except Exception as e:
        print(f"Error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(run())
