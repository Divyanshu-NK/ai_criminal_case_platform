from pydantic import BaseModel, Field
from typing import List
from app.models.context import Fact, Event, Entity

class FactExtractionSchema(BaseModel):
    facts: List[Fact] = Field(description="List of extracted facts from the scenario")
    timeline: List[Event] = Field(description="Timeline of events based on the facts")
    entities: List[Entity] = Field(description="List of entities (people, objects, locations) involved")
