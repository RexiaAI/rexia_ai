"""buffer manager class for ReXia.AI."""
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings

THOUGHT_BUFFER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "buffer")
THOUGHT_BUFFER_NAME = "thought_buffer"
MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
MODEL_KWARGS = {'device': 'cuda'}
ENCODE_KWARGS = {'normalize_embeddings': False}
SIMILARITY_THRESHOLD = 0.3

class BufferManager:
    """BufferManager class for ReXia AI."""
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BufferManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.qdrant_client = QdrantClient(path=THOUGHT_BUFFER_PATH)
        self.embeddings = HuggingFaceEmbeddings(
            model_name=MODEL_NAME,
            model_kwargs=MODEL_KWARGS,
            encode_kwargs=ENCODE_KWARGS
        )
        self._get_or_create_buffer()
        self._initialized = True

    def _get_or_create_buffer(self):
        """Get or create the Qdrant buffer."""
        if not self.qdrant_client.collection_exists(THOUGHT_BUFFER_NAME):
            # Embed a single document to get the vector size
            partial_embeddings = self.embeddings.embed_documents([""])
            vector_size = len(partial_embeddings[0])

            # Create the collection with the inferred vector size
            self.qdrant_client.recreate_collection(
                collection_name=THOUGHT_BUFFER_NAME,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

    def insert_or_update_plan(self, task: str, plan: str):
        """Insert or update a plan in the thought_buffer."""
        try:
            task_embedding = self.embeddings.embed_documents([task])[0]
            plan_embedding = self.embeddings.embed_documents([plan])[0]

            # Get information about the collection
            collection_info = self.qdrant_client.get_collection(THOUGHT_BUFFER_NAME)

            # Check if a plan for the current task exists in the thought_buffer
            results = self.qdrant_client.search(
                collection_name=THOUGHT_BUFFER_NAME,
                query_vector=task_embedding,
                limit=1
            )

            if results:
                # If a plan exists, update it
                vector_id = results[0].id if results[0].id is not None else 0
                point = PointStruct(
                    id=vector_id,
                    vector=plan_embedding,
                    payload={"task": task, "plan": plan}
                )
            else:
                # If no plan exists, create a new one
                vector_id = collection_info.vectors_count if collection_info.vectors_count is not None else 0
                point = PointStruct(
                    id=vector_id,
                    vector=plan_embedding,
                    payload={"task": task, "plan": plan}
                )

            self.qdrant_client.upsert(
                collection_name=THOUGHT_BUFFER_NAME,
                points=[point]
            )
        except ValueError as e:
            print(f"Value error occurred: {e}")
        except TypeError as e:
            print(f"Type error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_template(self, task: str):
        """Get the most similar template to the given task."""
        # Convert the task into an embedding
        thought_embedding = self.embeddings.embed_documents([task])[0]

        # Use the Qdrant client to find the most similar templates
        results = self.qdrant_client.search(
            collection_name=THOUGHT_BUFFER_NAME,
            query_vector=thought_embedding,
            limit=1
        )

        # If the similarity score of the most similar template is above the threshold, return the template
        if results[0].score >= SIMILARITY_THRESHOLD:
            return results[0]
        else:
            print("No template found with similarity above the threshold.")
            return None

    def delete_collection(self):
        """Delete the existing Qdrant collection. WARNING: This will delete all data in the collection.
        Only use this method if you are sure you want to delete the collection."""
        self.qdrant_client.delete_collection(collection_name=THOUGHT_BUFFER_NAME)