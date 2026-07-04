from typing import List
from app.models.context import Law

class LawRetrieverService:
    def retrieve_laws(self, search_terms: List[str]) -> List[Law]:
        """
        Mocked retrieval for Version 1.
        In a real scenario, this would query Qdrant using embeddings of the offence description or exact section matches.
        """
        mock_db = {
            "murder": Law(act_name="BNS", section="103", text="Punishment for murder...", ingredients=["Death of a person", "Intention to cause death"]),
            "theft": Law(act_name="BNS", section="303", text="Punishment for theft...", ingredients=["Dishonest intention", "Moving movable property out of possession"]),
            "hurt": Law(act_name="BNS", section="115", text="Voluntarily causing hurt...", ingredients=["Voluntary act", "Causing hurt to a person"]),
            "assault": Law(act_name="BNS", section="115", text="Voluntarily causing hurt...", ingredients=["Voluntary act", "Causing hurt to a person"])
        }
        
        results = []
        for term in search_terms:
            for k, v in mock_db.items():
                if k in term.lower() or v.section in term:
                    results.append(v)
        
        if not results:
            results.append(Law(act_name="BNS", section="Unknown", text="Mocked general provision", ingredients=["Actus Reus", "Mens Rea"]))
            
        return results

from app.models.context import SimilarCase

class CaseRetrieverService:
    def retrieve_cases(self, search_terms: List[str]) -> List[SimilarCase]:
        mock_cases = [
            SimilarCase(case_name="State vs X", court="Supreme Court", year=2015, summary="Precedent on circumstantial evidence in assault", relevance="High"),
            SimilarCase(case_name="Y vs State", court="High Court", year=2020, summary="Theft of movable property elements", relevance="Medium")
        ]
        return mock_cases

