from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def get_user_data(username:str,tool_context: ToolContext) -> dict:
    """Get user data from the database.
    
    Args:
        username: The username to retrieve data for
        tool_context: Context for accessing and updating session state

    Returns:
        User data dictionary
    """

    # Get user data from database
    user_data = tool_context.state.get("user", {}).get(username, {})

    return user_data

def save_user_data(username: str, password: str, personal_data: dict, tool_context: ToolContext) -> dict:
    """Save complete user data to the database for authentication and security verification.

    Args:
        username: The unique username for the account
        password: The user's password (will be encrypted before storage)
        personal_data: Dictionary containing all personal security questions and answers:
            - age: User's age
            - favorite_color: User's favorite color
            - favorite_team: User's favorite sports team
            - birth_city: City where user was born
            - first_pet_name: Name of user's first pet
            - mother_maiden_name: User's mother's maiden name
            - favorite_food: User's favorite food
            - elementary_school: Name of user's elementary school
            - favorite_movie: User's favorite movie
            - dream_vacation: User's dream vacation destination
            - Any additional custom security questions
        tool_context: Context for accessing and updating session state

    Returns:
        A confirmation message with account creation status"""

    user_record = {
        "username": username,
        "password": password,
        "personal_data": personal_data,
        "created_at": str(__import__('datetime').datetime.now()),
        "last_login": None,
        "failed_attempts": 0,
        "account_locked": False
    }

    if "user" not in tool_context.state:
        tool_context.state["user"] = {}

    tool_context.state["user"] = user_record

    return {
        "status": "success",
        "message": f"Account created successfully for username '{username}'. You can now log in with your credentials.",
        "username": username,
        "security_questions_count": len(personal_data)
    }

def authenticate_user(username: str, password: str, tool_context: ToolContext) -> dict:
    """Authenticate user with username and password, setting validation state.

    Args:
        username: The username to authenticate
        password: The password to verify
        tool_context: Tool context for state management

    Returns:
        Authentication result with validation status"""

    user_data = tool_context.state.get("user", {})

    if not user_data or user_data.get("username") != username:
        # Set validation state to false
        tool_context.state["validated"] = False
        tool_context.state["authentication_attempts"] = tool_context.state.get("authentication_attempts", 0) + 1
        return {
            "status": "failed",
            "message": "Username not found. Please check your username or create a new account.",
            "validated": False
        }

    if user_data.get("password") != password:
        # Set validation state to false
        tool_context.state["validated"] = False
        tool_context.state["authentication_attempts"] = tool_context.state.get("authentication_attempts", 0) + 1
        return {
            "status": "failed",
            "message": "Incorrect password. You can request a password reset if you've forgotten your password.",
            "validated": False
        }

    # Successful authentication - set validation state to true
    tool_context.state["validated"] = True
    tool_context.state["current_user"] = username
    tool_context.state["authentication_attempts"] = 0
    user_data["last_login"] = str(__import__('datetime').datetime.now())

    return {
        "status": "success",
        "message": f"Authentication successful! Welcome back, {username}. You now have access to your password manager.",
        "validated": True,
        "username": username
    }

def reset_password_with_verification(username: str, new_password: str, verification_answers: dict, tool_context: ToolContext) -> dict:
    """Reset user password after personal verification questions.

    Args:
        username: The username for password reset
        new_password: The new password to set
        verification_answers: Dictionary of answers to personal questions
        tool_context: Tool context for state management

    Returns:
        Password reset result with validation status"""

    user_data = tool_context.state.get("user", {})

    if not user_data or user_data.get("username") != username:
        tool_context.state["validated"] = False
        return {
            "status": "failed",
            "message": "Username not found.",
            "validated": False
        }

    stored_personal_data = user_data.get("personal_data", {})

    # Calculate verification score based on answer similarity
    total_questions = len(stored_personal_data)
    correct_answers = 0

    for question, stored_answer in stored_personal_data.items():
        user_answer = verification_answers.get(question, "").lower().strip()
        stored_answer_lower = str(stored_answer).lower().strip()

        if user_answer == stored_answer_lower or user_answer in stored_answer_lower or stored_answer_lower in user_answer:
            correct_answers += 1

    confidence_score = (correct_answers / total_questions * 100) if total_questions > 0 else 0

    if confidence_score >= 80:
        # High confidence - allow password reset
        user_data["password"] = new_password
        tool_context.state["validated"] = True
        tool_context.state["current_user"] = username
        tool_context.state["password_reset_in_progress"] = False

        return {
            "status": "success",
            "message": f"Password reset successful! Your new password has been set. You are now authenticated and can access your password manager.",
            "validated": True,
            "confidence_score": confidence_score
        }
    elif confidence_score >= 60:
        # Medium confidence - ask for additional verification
        tool_context.state["validated"] = False
        tool_context.state["password_reset_in_progress"] = True

        return {
            "status": "partial",
            "message": f"Partial verification successful (confidence: {confidence_score:.1f}%). Please answer additional questions for complete verification.",
            "validated": False,
            "confidence_score": confidence_score,
            "requires_additional_verification": True
        }
    else:
        # Low confidence - deny access
        tool_context.state["validated"] = False
        tool_context.state["password_reset_in_progress"] = False

        return {
            "status": "failed",
            "message": f"Verification failed (confidence: {confidence_score:.1f}%). Your answers don't match our records sufficiently.",
            "validated": False,
            "confidence_score": confidence_score
        }

AuthManager = Agent(
    name="Auth_Manager",
    model="gemini-2.0-flash",
    description="Intelligent authentication manager that secures user accounts through multi-layered personal verification. Maintains a comprehensive database of user credentials and personal security questions to enable secure password recovery through identity verification.",
    instruction="""
    You are an intelligent Authentication Manager in a SEQUENTIAL AGENT SYSTEM. You are the FIRST agent that runs and must set the 'validated' state to control access to the password manager.

    ## CRITICAL: Sequential Flow Control
    - You MUST set tool_context.state["validated"] = True for successful authentication
    - You MUST set tool_context.state["validated"] = False for failed authentication
    - The next agent (PasswordsManager) will ONLY run if validated = True
    - Use the authenticate_user tool to properly set validation state

    ## Core Responsibilities:
    1. **User Database Management**: Maintain a secure database containing:
       - Username and password
       - Personal security questions and answers
       - User profile data (age, favorite color, favorite team, etc.)

    2. **Account Creation Process** (for first-time user):
       When a user doesn't have an account yet:

       a) **Initial Setup**: Collect basic account information:
          - Username (check for uniqueness)
          - Password (ensure strong password requirements)
          - Email address

       b) **Personal Security Questions Setup**: Ask and store answers to security questions:
          - "What is your age?"
          - "What is your favorite color?"
          - "What is your favorite sports team?"
          - "What city were you born in?"
          - "What was your first pet's name?"
          - "What is your mother's maiden name?"
          - "What is your favorite food?"
          - "What was the name of your elementary school?"
          - "What is your favorite movie?"
          - "What is your dream vacation destination?"
          - And any other custom personal questions you want to add

       c) **Data Storage**: Use the available tools to securely save all user information:
          - Store encrypted password
          - Save all personal security questions and answers
          - Create user profile with personal data
          - Initialize authentication history

    3. **Authentication Process**:
       - Check if user exists in database first using available tools
       - If user doesn't exist, initiate account creation process
       - If user exists, verify credentials during login attempts
       - Handle password reset requests securely

    ## Tool Usage Guidelines:
    - Always use the provided tools to interact with the database
    - Call appropriate tools for user lookup, creation, and data storage
    - Ensure all data is properly encrypted before storage
    - Use tools to verify user existence before proceeding with authentication or account creation

    4. **Password Recovery Through Personal Verification**:
       When a user forgets their password, conduct a comprehensive identity verification process:

       a) **Initial Verification**: Ask for basic identifying information (username, email)

       b) **Personal Security Questions**: Present a series of personal questions from the database:
          - "What is your age?"
          - "What is your favorite color?"
          - "What is your favorite sports team?"
          - "What city were you born in?"
          - "What was your first pet's name?"
          - "What is your mother's maiden name?"
          - And other custom personal questions stored in their profile

       c) **Answer Analysis**:
          - Compare user responses with stored answers
          - Use fuzzy matching for slight variations (typos, different formatting)
          - Calculate confidence score based on answer accuracy
          - Consider partial matches (e.g., "blue" vs "dark blue")

       d) **Decision Making**:
          - If confidence score >= 80%: Allow password reset
          - If confidence score 60-79%: Ask additional verification questions
          - If confidence score < 60%: Deny access and log security event

    ## Security Protocols:
    - Implement rate limiting for failed attempts
    - Never reveal stored answers, only verify against them
    - Use secure random questions selection to prevent pattern recognition
    - Maintain audit trail of all password recovery attempts

    ## Response Guidelines:
    - Be professional and security-conscious
    - Explain verification steps clearly to user
    - Provide helpful feedback without compromising security
    - Guide user through the recovery process step-by-step
    - Alert user to suspicious activity on their accounts

    ## Error Handling:
    - Handle database connection issues gracefully
    - Provide clear error messages without revealing system details
    - Implement fallback verification methods when needed
    - Escalate to human administrators for complex cases

    ## Workflow for New User:
    1. **User Interaction**: When a user attempts to log in or requests access
    2. **User Lookup**: Use tools to check if username exists in database
    3. **New User Detection**: If user not found, explain account creation process
    4. **Account Creation**: Guide user through complete setup:
       - Collect username, password, email
       - Ask all personal security questions one by one
       - Confirm all information before saving
    5. **Data Persistence**: Use tools to save all collected information securely
    6. **Confirmation**: Confirm successful account creation and guide to login

    ## Workflow for Existing User:
    1. **Authentication**: Verify username and password using tools
    2. **Success**: Grant access if credentials are correct
    3. **Password Recovery**: If password forgotten, initiate personal verification process

    Remember: Security is paramount. When in doubt, err on the side of caution and require additional verification. Always use the provided tools for database operations.
    """,
    tools=[get_user_data, save_user_data, authenticate_user, reset_password_with_verification],
)