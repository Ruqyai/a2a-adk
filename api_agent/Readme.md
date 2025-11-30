
# ADK Agent Example

This project demonstrates how to set up and interact with a **Google ADK agent** (`use_api_agent`) using the in-memory session service. You can create sessions, send messages, and receive stateful responses from your agent.

---

## Prerequisites

- Python 3.13+
- ADK installed in a virtual environment (`.venv`)
- Required packages installed (check your `requirements.txt`)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

---

## 1. Start the ADK API Server

Run the server from your project root (parent folder containing your agent folder):

```bash
adk api_server my_agent
```

Expected output:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

> **Note:** Make sure port `8000` is free. If not, kill existing processes:
>
> ```bash
> kill -9 $(lsof -t -i :8000)
> ```

---

## 2. Create a Session

You must create a session before sending messages. Replace `<agent_name>`, `<user_id>`, and `<session_id>` with your values:

```bash
curl -X POST http://localhost:8000/apps/use_api_agent/users/u_123/sessions/s_run_test \
-H "Content-Type: application/json" \
-d '{
  "role": "user",
  "parts": [{"text": "Create session first"}]
}'
```

Expected response:

```json
{
  "id": "s_run_test",
  "appName": "use_api_agent",
  "userId": "u_123",
  "state": {"role":"user","parts":[{"text":"Create session first"}]},
  "events": [],
  "lastUpdateTime": 1764423430.2701151
}
```

---

## 3. Send Messages to the Agent

Once the session is created, you can send messages to the agent:

```bash
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{
  "appName": "use_api_agent",
  "userId": "u_123",
  "sessionId": "s_run_test",
  "newMessage": {
    "role": "user",
    "parts": [{"text": "Hello! What can you help me with?"}]
  }
}'
```

Example agent response:

```json
[{
  "modelVersion": "gemini-2.5-flash",
  "content": {
    "parts": [{"text": "Hello! How can I help you today?"}],
    "role": "model"
  },
  "finishReason": "STOP"
}]
```

---

## 4. Send Follow-up Messages

You can continue the conversation using the **same session**:

```bash
curl -X POST http://localhost:8000/run \
-H "Content-Type: application/json" \
-d '{
  "appName": "use_api_agent",
  "userId": "u_123",
  "sessionId": "s_run_test",
  "newMessage": {
    "role": "user",
    "parts": [{"text": "Can you tell me more about your capabilities?"}]
  }
}'
```

The agent will respond with a detailed answer, remembering the previous message in the same session.

---

## 5. Notes

* **Sessions must be created first** — otherwise `/run` will return `"Session not found"`.
* Always use the **full session creation endpoint** format:

```
/apps/<agent_name>/users/<user_id>/sessions/<session_id>
```

* The in-memory session service is **temporary**; session data will be lost if the server restarts. Use a persistent session service for production.

---

## 6. Troubleshooting

1. **Port 8000 already in use:**

```bash
kill -9 $(lsof -t -i :8000)
```

2. **Agent not found error:**

* Ensure your agent folder contains either:

  * `agent.py` with `root_agent` defined, OR
  * `root_agent.yaml`
* Run the API server from the **parent folder** of your agent folder.

3. **Session not found:**

* Make sure to create a session before sending messages.




