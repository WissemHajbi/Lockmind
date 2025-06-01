from google.adk.agents import SequentialAgent

from .workers.auth_manager import AuthManager
from .workers.passwords_manager import PasswordsManager

LockmindAgent = SequentialAgent(
    name="Lockmind_Sequential_Agent",
    sub_agents=[AuthManager, PasswordsManager],
    description="Sequential authentication system that requires authentication before password management access",
)
