import asyncio
from dotenv import load_dotenv
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from Agency import LockmindAgent
from google.genai import types

load_dotenv()

db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)


initial_state = {
    "passwords": [],
    "validated": False,
    "current_user": None,
    "authentication_attempts": 0,
    "password_reset_in_progress": False,
}

async def main_async():
    new_session = session_service.create_session(
        app_name="Lockmind",
        user_id="ThisIsMyId",
        state=initial_state,
    )

    runner = Runner(
        agent=LockmindAgent,
        app_name="Lockmind",
        session_service=session_service,
    )
    
    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Goodbye!")
            break

        content = types.Content(role="user", parts=[types.Part(text=user_input)])

        try:   
            async for event in runner.run_async(user_id="ThisIsMyId", session_id=new_session.id, new_message=content):
                if event.content and event.content.parts and event.content.parts[0].text:
                    print(f"AI: {event.content.parts[0].text}")
        except Exception as e:
            print(f"Error during agent run: {e}")


if __name__ == "__main__":
    asyncio.run(main_async())