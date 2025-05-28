from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def get_passwords(tool_context: ToolContext) -> dict:
    """Get passwords from the database."""

    passwords = tool_context.state.get("passwords", [])

    return passwords

def add_password(service_name: str, username: str, password: str, tool_context: ToolContext) -> dict:
    """Add a password to the database."""

    password_record = {
        "service": service_name,
        "username": username,
        "password": password,
    }

    if "passwords" not in tool_context.state:
        tool_context.state["passwords"] = []

    tool_context.state["passwords"].append(password_record)

    return {
        "status": "success",
        "message": f"Password added successfully for service '{service_name}'.",
        "service_name": service_name,
        "username": username
    }

def modify_password(service_name: str, username: str, new_password: str, tool_context: ToolContext) -> dict:
    """Modify a password in the database."""

    passwords = tool_context.state.get("passwords", [])

    for password in passwords:
        if password["service"] == service_name and password["username"] == username:
            password["password"] = new_password
            tool_context.state["passwords"] = passwords
            return {
                "status": "success",
                "message": f"Password modified successfully for service '{service_name}'.",
                "service_name": service_name,
                "username": username
            }

    return {
        "status": "error",
        "message": f"Password not found for service '{service_name}' and username '{username}'.",
        "service_name": service_name,
        "username": username
    }

def remove_password(service_name: str, username: str, tool_context: ToolContext) -> dict:
    """Remove a password from the database."""

    passwords = tool_context.state.get("passwords", [])

    for password in passwords:
        if password["service"] == service_name and password["username"] == username:
            passwords.remove(password)
            tool_context.state["passwords"] = passwords
            return {
                "status": "success",
                "message": f"Password removed successfully for service '{service_name}'.",
                "service_name": service_name,
                "username": username
            }

    return {
        "status": "error",
        "message": f"Password not found for service '{service_name}' and username '{username}'.",
        "service_name": service_name,
        "username": username
    }

PasswordsManager = Agent(   
    name="Passwords_Manager",
    model="gemini-2.0-flash",
    description="passwords manager that add and remove and edit and get passwords.",
    instruction="""
    You are an  Passwords Manager responsible for

    ## Core Responsibilities:
    1. **User Database Management**: Maintain a secure database containing:
       - Service name
       - Username and password
    
    2. **Password Management**:
       - Add new passwords
       - Modify existing passwords
       - Remove passwords
       - Get passwords

    3. **Password Verification**:
       - Verify passwords before adding or modifying
       - Ensure strong password requirements

    """,
    tools=[get_passwords, add_password, modify_password, remove_password],
)