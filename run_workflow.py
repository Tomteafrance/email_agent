from src.agents.graph import workflow

config = {"configurable": {"langgraph_user_id": "lance"}}
email_input = {
    "author": "Alice Smith <alice.smith@company.com>",
    "to": "John Doe <john.doe@company.com>",
    "subject": "Quick question about API documentation",
    "email_thread": """Hi John,

I was reviewing the API documentation for the new authentication service and noticed a few endpoints seem to be missing from the specs. Could you help clarify if this was intentional or if we should update the docs?

Specifically, I'm looking at:
- /auth/refresh
- /auth/validate

Thanks!
Alice""",
}

response = workflow.invoke(
    {"email_input": email_input},
    config=config
)

for m in response["messages"]:
    m.pretty_print()

email_input = {
    "author": "Alice Smith <alice.smith@company.com>",
    "to": "John Doe <john.doe@company.com>",
    "subject": "Follow up",
    "email_thread": """Hi John,

Any update on my previous ask?""",
}

response = workflow.invoke({"email_input": email_input}, config=config)

for m in response["messages"]:
    m.pretty_print()


