STRATEGY_PROMPT = """
You are a top-tier criminal defense and prosecution strategist.
Based on the validated charges, missing evidence, and similar cases, formulate the arguments for BOTH prosecution and defense. Also identify key weaknesses in the case.

Validated Charges:
{validation}

Missing Evidence:
{missing_evidence}

Similar Cases:
{similar_cases}
"""
