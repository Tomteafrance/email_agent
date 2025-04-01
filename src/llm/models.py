from pydantic import BaseModel
from langchain_ollama import ChatOllama

class LLMModel(BaseModel):
    """Represents an LLM Model"""
    def get_model_list(self):
        return [
            "qwen2.5:7b",
            "llama3.2:latest"
        ]

    def get_model(self, model_name: str) -> ChatOllama:
        return ChatOllama(model=model_name)
