from typing import Any, List
from pydantic import BaseModel
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from src.agents.prompts import PromptTemplate
from src.agents.utils import profile, prompt_instructions

class EmailAgent(BaseModel):
    llm: ChatOllama
    tools: List[Any]

    def create_prompt(self, state):
            return [
            {
                "role": "system", 
                "content": PromptTemplate.get_agent_system_prompt().format(
                    instructions=prompt_instructions["agent_instructions"],
                    **profile
                    )
            }
        ] + state['messages']
    
    def create_agent(self):
        return create_react_agent(
                    self.llm,
                    tools=self.tools,
                    prompt=self.create_prompt,
                )
        