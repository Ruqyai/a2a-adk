"""
Copyright 2025 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import gradio as gr

from typing import List, Dict, Any
from pprint import pformat
from purchasing_concierge.agent import root_agent as LOCAL_AGENT
import os
from dotenv import load_dotenv

load_dotenv()

USER_ID = "default_user"


async def get_response_from_agent(
    message: str,
    history: List[Dict[str, Any]],
) -> str:
    """Send the message to the backend and get a response.

    Args:
        message: Text content of the message.
        history: List of previous message dictionaries in the conversation.

    Returns:
        Text response from the backend service.
    """
    default_response = "No response from agent"

    responses = []

    for event in LOCAL_AGENT.query(message=message):
        if "output" in event:
            responses.append(
                gr.ChatMessage(
                    role="assistant",
                    content=event["output"],
                )
            )
        if "tool_code" in event and event["tool_code"]:
            responses.append(
                gr.ChatMessage(
                    role="assistant",
                    content=f"```python\n{event['tool_code']}\n```",
                    metadata={"title": "🛠️ Tool Call"},
                )
            )
        if "tool_result" in event and event["tool_result"]:
            tool_result = event["tool_result"]
            if isinstance(tool_result, list):
                tool_result = "\n".join(
                    [
                        f"```python\n{pformat(r, indent=2, width=80)}\n```"
                        for r in tool_result
                    ]
                )
            else:
                tool_result = f"```python\n{pformat(tool_result, indent=2, width=80)}\n```"
            responses.append(
                gr.ChatMessage(
                    role="assistant",
                    content=tool_result,
                    metadata={"title": "⚡ Tool Response"},
                )
            )

    if not responses:
        yield default_response

    yield responses


if __name__ == "__main__":
    demo = gr.ChatInterface(
        get_response_from_agent,
        title="Purchasing Concierge",
        description="This assistant can help you to purchase food from remote sellers.",
        type="messages",
    )

    demo.launch(
        server_name="0.0.0.0",
        server_port=8080,
    )
