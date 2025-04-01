from typing_extensions import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from src.agents.agent import EmailAgent
from src.agents.state import Router, State
from src.agents.prompts import PromptTemplate
from src.agents.tools import AgentTool
from src.agents.utils import profile, prompt_instructions
from src.llm.models import LLMModel

llm = LLMModel().get_model("qwen2.5:7b")
llm_router = llm.with_structured_output(Router)
tools = [AgentTool.write_email, AgentTool.schedule_meeting, AgentTool.check_calendar_availability]

def triage_router(state: State) -> Command[
    Literal["response_agent", "__end__"]
]:
    author = state['email_input']['author']
    to = state['email_input']['to']
    subject = state['email_input']['subject']
    email_thread = state['email_input']['email_thread']

    system_prompt = PromptTemplate.get_triage_system_prompt().format(
        full_name=profile["full_name"],
        name=profile["name"],
        user_profile_background=profile["user_profile_background"],
        triage_no=prompt_instructions["triage_rules"]["ignore"],
        triage_notify=prompt_instructions["triage_rules"]["notify"],
        triage_email=prompt_instructions["triage_rules"]["respond"],
        examples=None
    )
    user_prompt = PromptTemplate.get_triage_user_prompt().format(
        author=author, 
        to=to, 
        subject=subject, 
        email_thread=email_thread
    )
    result = llm_router.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )
    if result.classification == "respond":
        print("📧 Classification: RESPOND - This email requires a response")
        goto = "response_agent"
        update = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Respond to the email {state['email_input']}",
                }
            ]
        }
    elif result.classification == "ignore":
        print("🚫 Classification: IGNORE - This email can be safely ignored")
        update = None
        goto = END
    elif result.classification == "notify":
        print("🔔 Classification: NOTIFY - This email contains important information")
        update = None
        goto = END
    else:
        raise ValueError(f"Invalid classification: {result.classification}")
    return Command(goto=goto, update=update)

email_agent = EmailAgent(llm=llm, tools=tools)
react_agent = email_agent.create_agent()
workflow = StateGraph(State)
workflow = workflow.add_node(triage_router)
workflow = workflow.add_node("response_agent", react_agent)
workflow = workflow.add_edge(START, "triage_router")
workflow = workflow.compile()
