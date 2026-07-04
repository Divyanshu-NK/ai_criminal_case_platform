SCENARIO_PARSER_PROMPT = """
You are an expert legal assistant. Your task is to clean and standardize the following raw scenario.
Ensure it is written in a clear, objective, and chronological narrative suitable for legal analysis.
Identify the jurisdiction if apparent (default to India if not specified).

Raw Scenario:
{scenario}

Output the cleaned narrative and jurisdiction strictly according to the schema.
"""
