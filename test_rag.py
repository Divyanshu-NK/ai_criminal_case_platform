import asyncio
import sys
from app.rag.retrieval import LawRetrieverService, CaseRetrieverService
import logging

logging.basicConfig(level=logging.INFO)

def test_rag():
    print("Testing LawRetrieverService...")
    law_retriever = LawRetrieverService()
    search_terms = ["murder and death", "voluntarily causing hurt"]
    laws = law_retriever.retrieve_laws(search_terms)
    
    print(f"Retrieved {len(laws)} unique laws.")
    for law in laws:
        print(f"- BNS {law.section}: {law.text[:200]}...")
        print(f"  Ingredients: {law.ingredients}")

    print("\nTesting CaseRetrieverService...")
    case_retriever = CaseRetrieverService()
    case_search_terms = ["murder appeal", "bail in criminal case"]
    cases = case_retriever.retrieve_cases(case_search_terms)
    
    print(f"Retrieved {len(cases)} unique supreme court cases.")
    for case in cases:
        print(f"- {case.case_name} ({case.court})")
        print(f"  Summary: {case.summary}")

if __name__ == "__main__":
    test_rag()
