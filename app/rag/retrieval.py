import logging
from typing import List
from app.models.context import Law, SimilarCase
from app.rag.qdrant import qdrant_manager
from app.rag.embedding.service import embedding_service

logger = logging.getLogger("agent_logger")

class LawRetrieverService:
    def __init__(self):
        self.client = qdrant_manager.get_client()
        self.collection_name = "bns_laws"
        
    def retrieve_laws(self, search_terms: List[str], top_k: int = 3) -> List[Law]:
        """
        Queries Qdrant for relevant laws based on embeddings of search terms.
        """
        results = []
        seen_sections = set()
        
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except Exception:
            logger.warning(f"Collection {self.collection_name} does not exist. Returning empty laws.")
            return []

        for term in search_terms:
            vector = embedding_service.embed_text(term)
            try:
                search_result = self.client.query_points(
                    collection_name=self.collection_name,
                    query=vector,
                    limit=top_k
                ).points
                
                for hit in search_result:
                    payload = hit.payload
                    section_key = f"{payload['act_name']}_{payload['section']}"
                    
                    if section_key not in seen_sections:
                        seen_sections.add(section_key)
                        results.append(
                            Law(
                                act_name=payload["act_name"],
                                section=payload["section"],
                                text=payload["text"],
                                ingredients=payload.get("ingredients", [])
                            )
                        )
            except Exception as e:
                logger.error(f"Error searching Qdrant: {e}")
                
        return results


class CaseRetrieverService:
    def __init__(self):
        self.client = qdrant_manager.get_client()
        self.collection_name = "supreme_court_cases"
        
    def retrieve_cases(self, search_terms: List[str], top_k: int = 3) -> List[SimilarCase]:
        results = []
        seen_cases = set()
        
        try:
            # Check if collection exists
            self.client.get_collection(self.collection_name)
        except Exception:
            logger.warning(f"Collection {self.collection_name} does not exist. Returning empty cases.")
            return []

        for term in search_terms:
            vector = embedding_service.embed_text(term)
            try:
                search_result = self.client.query_points(
                    collection_name=self.collection_name,
                    query=vector,
                    limit=top_k
                ).points
                
                for hit in search_result:
                    payload = hit.payload
                    case_key = payload['case_id']
                    
                    if case_key not in seen_cases:
                        seen_cases.add(case_key)
                        results.append(
                            SimilarCase(
                                case_name=payload["title"],
                                court=payload["court"],
                                year=2024, # Mocked since not extracted explicitly
                                summary=payload["text"][:300] + "...", # Truncated summary
                                relevance="High" # Semantic search guarantees some relevance
                            )
                        )
            except Exception as e:
                logger.error(f"Error searching Qdrant for cases: {e}")
                
        return results
