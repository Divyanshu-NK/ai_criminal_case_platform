EVIDENCE_BUILDER_PROMPT = """
You are an evidence extraction expert. Given a set of facts, identify any physical, documentary, or testimonial evidence mentioned or strongly implied.

Facts:
{facts}

Extract evidence into a structured format and link it to the relevant fact IDs. Assign a unique ID to each piece of evidence.
"""
