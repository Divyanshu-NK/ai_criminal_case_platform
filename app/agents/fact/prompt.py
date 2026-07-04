FACT_EXTRACTION_PROMPT = """
You are a legal fact extractor. Your job is to extract structured facts, timeline events, and entities from a raw criminal scenario.

Given the following scenario:
{scenario}

Extract the facts, timeline, and entities strictly in the provided JSON schema.
- Assign unique IDs to facts and entities.
- Timeline events should reference fact IDs if applicable.
- Give a confidence score (0.0 to 1.0) for each fact.
"""
