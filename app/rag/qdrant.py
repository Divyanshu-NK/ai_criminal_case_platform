import logging
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from app.core.config import settings

logger = logging.getLogger("agent_logger")

class QdrantManager:
    def __init__(self):
        # Uses local disk storage instead of a Docker container
        self.client = QdrantClient(path="./qdrant_data")
        self.vector_size = 384 # Since we use all-MiniLM-L6-v2
        
    def create_collection(self, collection_name: str):
        """Creates a collection if it doesn't exist."""
        try:
            self.client.get_collection(collection_name)
            logger.info(f"Collection '{collection_name}' already exists.")
        except Exception:
            logger.info(f"Creating collection '{collection_name}'...")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=rest.VectorParams(
                    size=self.vector_size,
                    distance=rest.Distance.COSINE
                )
            )
            
    def get_client(self) -> QdrantClient:
        return self.client

qdrant_manager = QdrantManager()
