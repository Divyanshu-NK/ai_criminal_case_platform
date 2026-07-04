from typing import List
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the local sentence-transformer model.
        all-MiniLM-L6-v2 is lightweight and maps sentences to a 384 dimensional dense vector space.
        """
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers is not installed. Please install it to use local embeddings.")
        self.model = SentenceTransformer(model_name)
        
    def embed_text(self, text: str) -> List[float]:
        """Embeds a single string into a vector."""
        return self.model.encode(text).tolist()
        
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embeds a batch of strings into vectors."""
        return self.model.encode(texts).tolist()

# Singleton instance for the app
embedding_service = EmbeddingService()
