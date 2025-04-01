from langchain_core.tools import tool
from langchain_core.tools.structured import StructuredTool
from langmem import create_manage_memory_tool, create_search_memory_tool

class AgentTool():
    @tool
    def write_email(to: str, subject: str, content: str) -> str:
        """Write and send an email."""
        # Placeholder response - in real app would send email
        return f"Email sent to {to} with subject '{subject}'"


    @tool
    def schedule_meeting(
        attendees: list[str], 
        subject: str, 
        duration_minutes: int, 
        preferred_day: str
    ) -> str:
        """Schedule a calendar meeting."""
        return f"Meeting '{subject}' scheduled for {preferred_day} with {len(attendees)} attendees"

    @tool
    def check_calendar_availability(day: str) -> str:
        """Check calendar availability for a given day."""
        return f"Available times on {day}: 9:00 AM, 2:00 PM, 4:00 PM"

    def manage_memory_tool() -> StructuredTool:
        """ manage memory for tool"""
        return create_manage_memory_tool(
            namespace=(
                "email_assistant", 
                "{langgraph_user_id}",
                "collection"
            )
        )
    
    def search_memory_tool() -> StructuredTool:
        """ search memory for tool"""
        return create_search_memory_tool(
            namespace=(
                "email_assistant",
                "{langgraph_user_id}",
                "collection"
            )
        )
