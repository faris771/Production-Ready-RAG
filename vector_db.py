from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import constants as const


#PointStruct → the data structure representing one stored vector + metadata.
# PointStruct: Represents a single “point” (vector) stored in Qdrant, along with metadata (payload) and an ID.

class QdrantStorage:
    # This is a wrapper around Qdrant to easily manage vector storage and retrieval.
    def __init__(self, url=const.QDRANT_URL, collection=const.COLLECTION_NAME, dim=const.EMBEDDING_DIM):

        self.client = QdrantClient(url=url, timeout=30)
        self.collection = collection

        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE)

            )


    def upsert(self, ids, vectors, payloads) -> None :
        points = [PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))]
        self.client.upsert(self.collection, points=points)


    def search(self, query_vector, top_k: int = 5): # WHY VECTOR?? because u decide what kind of embedding you will  use

        results = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,  # it was quer_vector
            limit=top_k,
            with_payload=True
        )
        contexts = []
        sources = []
        for r in results:
            payload = getattr(r, "payload", None) or {}
            text = payload.get("text", "")
            source = payload.get("source", "")
            if text:
                contexts.append(text)
                sources.append(source)

        return {"contexts": contexts, "sources": sources}
