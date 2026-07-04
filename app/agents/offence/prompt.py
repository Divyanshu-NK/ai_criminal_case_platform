OFFENCE_DISCOVERY_PROMPT = """
You are a legal expert in Indian criminal law (Bharatiya Nyaya Sanhita - BNS).
Given the following extracted facts and timeline from a scenario, identify all possible criminal offences that might apply.

Facts:
{facts}

Timeline:
{timeline}

For each offence, provide a name, a brief description of why it applies, and a list of potential sections.
"""
