from typing import List, Any
from langgraph.store.memory import InMemoryStore
import requests

def ollama_embedding(texts) -> List[Any]:
    url = "http://localhost:11434/api/embed"
    model_name = "all-minilm"
    data = {
        "model": model_name,
        "input": texts,
        "options": {"encoding_format": "float"}
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()["embeddings"]

class MemoryStore:
    def get_memory_store() -> InMemoryStore:
        return InMemoryStore(
                    index={
                        "embed": ollama_embedding
                    }
                )
