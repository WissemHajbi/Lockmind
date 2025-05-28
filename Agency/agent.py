from google.adk.agents import Agent

from .workers.auth_manager import AuthManager
from .workers.passwords_manager import PasswordsManager

ManagerAgent = Agent(
    name="Manager_agent",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.
    
    You are responsible for delegating tasks to the following agent:
    - auth_manager
    - passwords_manager

    at first you should delegate to the auth_manager to check if the user is authenticated.
    """,
    sub_agents=[AuthManager, PasswordsManager],
)
