from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class Fact(BaseModel):
    id: str = Field(..., description="Unique identifier for the fact")
    description: str = Field(..., description="Description of the fact extracted from scenario")
    confidence: float = Field(..., description="Confidence score of the extraction")

class Event(BaseModel):
    timestamp: str = Field(..., description="Time or sequence of the event")
    description: str = Field(..., description="What happened")
    related_facts: List[str] = Field(default_factory=list, description="IDs of related facts")

class Entity(BaseModel):
    id: str
    name: str
    role: str = Field(..., description="Role in the scenario, e.g., Victim, Accused, Witness")

class Evidence(BaseModel):
    id: str
    type: str = Field(..., description="Type of evidence, e.g., Physical, Testimonial, Documentary")
    description: str
    related_facts: List[str] = Field(default_factory=list)

class Offence(BaseModel):
    id: str
    name: str
    description: str
    potential_sections: List[str] = Field(default_factory=list)

class Law(BaseModel):
    act_name: str
    section: str
    text: str
    ingredients: List[str] = Field(default_factory=list)

class ValidationResult(BaseModel):
    is_satisfied: bool
    reasoning: str
    missing_ingredients: List[str] = Field(default_factory=list)

class MissingEvidence(BaseModel):
    description: str
    reason: str = Field(..., description="Why this evidence is needed based on missing ingredients")

class SimilarCase(BaseModel):
    case_name: str
    court: str
    year: int
    summary: str
    relevance: str

class Strategy(BaseModel):
    prosecution_arguments: List[str] = Field(default_factory=list)
    defense_arguments: List[str] = Field(default_factory=list)
    key_weaknesses: List[str] = Field(default_factory=list)

class LegalReport(BaseModel):
    summary: str
    recommended_charges: List[str] = Field(default_factory=list)
    procedural_next_steps: List[str] = Field(default_factory=list)
    conclusion: str

class CaseContext(BaseModel):
    scenario: str = Field(default="", description="The raw input scenario")
    facts: List[Fact] = Field(default_factory=list)
    timeline: List[Event] = Field(default_factory=list)
    entities: List[Entity] = Field(default_factory=list)
    evidence: List[Evidence] = Field(default_factory=list)
    offences: List[Offence] = Field(default_factory=list)
    laws: List[Law] = Field(default_factory=list)
    validation: Dict[str, ValidationResult] = Field(default_factory=dict)
    missing_evidence: List[MissingEvidence] = Field(default_factory=list)
    similar_cases: List[SimilarCase] = Field(default_factory=list)
    strategy: Optional[Strategy] = None
    procedural_steps: List[str] = Field(default_factory=list)
    report: Optional[LegalReport] = None
