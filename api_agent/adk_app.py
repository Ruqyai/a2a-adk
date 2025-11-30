from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from use_api_agent.agent import root_agent

APP_NAME = "use_api_agent"

# global session service
session_service = InMemorySessionService()

# global runner
runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service,
)

def handler(event):
    user_id = event.user_id
    session_id = event.session_id

    # create session if not exists
    session = session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )

    if session is None:
        session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
            state={},
        )

    # convert incoming message
    text = event.new_message.parts[0].text
    content = types.Content(
        parts=[types.Part(text=text)],
        role="user"
    )

    # run the agent
    for output in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=content
    ):
        if output.is_final_response():
            return {"text": output.content.parts[0].text}
