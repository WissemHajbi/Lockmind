from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def check_authentication_status(tool_context: ToolContext) -> dict:
    """Check if user is authenticated and authorized to access password manager.
    
    Args:
        tool_context: Context for accessing and updating session state

    Returns:
        Authentication status dictionary
    """

    validated = tool_context.state.get("validated", False)
    current_user = tool_context.state.get("current_user", None)

    if not validated:
        return {
            "status": "unauthorized",
            "message": "Access denied. You must authenticate first through the authentication system.",
            "authenticated": False
        }

    return {
        "status": "authorized",
        "message": f"Access granted. Welcome to your password manager, {current_user}!",
        "authenticated": True,
        "current_user": current_user
    }

def get_passwords(tool_context: ToolContext) -> dict:
    """Get passwords from the database. 
    
    Args:
        tool_context: Context for accessing and updating session state

    Returns:
        Passwords dictionary
    """

    # Check authentication first
    auth_check = check_authentication_status(tool_context)
    if not auth_check.get("authenticated", False):
        return auth_check

    passwords = tool_context.state.get("passwords", [])

    return {
        "status": "success",
        "passwords": passwords,
        "count": len(passwords)
    }

def add_password(service_name: str, username: str, password: str, tool_context: ToolContext) -> dict:
    """Add a password to the database.
    
    Args:
        service_name: The name of the service
        username: The username for the service
        password: The password for the service
        tool_context: Context for accessing and updating session state

    Returns:
        Password addition result
    """

    # Check authentication first
    auth_check = check_authentication_status(tool_context)
    if not auth_check.get("authenticated", False):
        return auth_check

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
    """Modify a password in the database.
    Args:
        service_name: The name of the service
        username: The username for the service
        new_password: The new password for the service
        tool_context: Context for accessing and updating session state

    Returns:
        Password modification result
    """

    # Check authentication first
    auth_check = check_authentication_status(tool_context)
    if not auth_check.get("authenticated", False):
        return auth_check

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
    """Remove a password from the database.
    
    Args:
        service_name: The name of the service
        username: The username for the service
        tool_context: Context for accessing and updating session state

    Returns:
        Password removal result
    """

    # Check authentication first
    auth_check = check_authentication_status(tool_context)
    if not auth_check.get("authenticated", False):
        return auth_check

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
    description="Secure password manager that requires authentication before providing access to password management features.",
    instruction="""
    You are a Passwords Manager that provides secure password management services.

    ## Core Responsibilities:
    1. **Password Management**:
       - Add new passwords
       - Modify existing passwords
       - Remove passwords
       - Get passwords

    2. **User Experience**:
       - Welcome authenticated users warmly
       - Provide helpful password management guidance
       - Help users organize and secure their passwords
       - Suggest strong password practices

    3. **Security**:
       - All tools include authentication checks
       - Maintain secure password storage
       - Provide strong password recommendations

    ## Note:
    You will only receive user messages when they are authenticated.
    The main system filters out your responses when users are not authenticated.
    Focus on providing excellent password management services!
    """,
    tools=[check_authentication_status, get_passwords, add_password, modify_password, remove_password],
)