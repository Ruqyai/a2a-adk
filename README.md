# Purchasing Concierge A2A Demo - Local Setup

> **⚠️ DISCLAIMER: THIS IS NOT AN OFFICIALLY SUPPORTED GOOGLE PRODUCT. THIS PROJECT IS INTENDED FOR DEMONSTRATION PURPOSES ONLY. IT IS NOT INTENDED FOR USE IN A PRODUCTION ENVIRONMENT.**

This demo shows how to enable A2A (Agent2Agent) protocol communication between purchasing concierge agent with the remote pizza and burger seller agents using A2A Python SDK. The system has been modified to use Gemini API instead of Vertex AI, allowing it to run locally without requiring Google Cloud infrastructure.

## Recent Changes

The codebase has been updated to replace Vertex AI usage with Gemini API:

- **Pizza Agent**: Now uses `ChatGoogleGenerativeAI` with `gemini-2.5-flash-lite` instead of `ChatVertexAI`
- **Burger Agent**: Now uses `gemini/gemini-2.5-flash-lite` model via LiteLLM instead of Vertex AI
- **Purchasing Concierge**: Now uses `gemini-2.5-flash` model
- **Deployment**: Removed Vertex AI deployment scripts - agents now run locally
- **Environment**: Updated to use `GOOGLE_API_KEY` (or `GEMINI_API_KEY` for Burger Agent) for Gemini API access

## Prerequisites

- Python 3.12 or higher
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for dependency management

### Install uv and Python

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.12
```

## Installation

1. Clone or navigate to the project directory
2. Install dependencies:

```shell
uv sync --frozen
```

**Important**: `uv` automatically manages virtual environments for you. You do NOT need to manually activate virtual environments with `source .venv/bin/activate` - just use `uv run` commands as shown in the steps below.

**Note**: If you encounter langgraph compatibility issues, the agents use specific versions:
- Pizza agent: `langgraph==1.0.4`
- Burger agent: Uses CrewAI with LiteLLM for Gemini API
- Both agents require: `a2a-sdk[http-server]` for the web server functionality

## Environment Setup

### Main Project .env

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your Gemini API key:

```bash
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_gemini_api_key_here
PIZZA_SELLER_AGENT_URL=http://localhost:10000
BURGER_SELLER_AGENT_URL=http://localhost:10001
```

### Agent Environment Files

The agent `.env` files are already configured with the necessary settings. They include:

For Pizza Agent:
```bash
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_gemini_api_key_here
HOST_OVERRIDE=http://localhost:10000
```

For Burger Agent:
```bash
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GEMINI_API_KEY=your_gemini_api_key_here
HOST_OVERRIDE=http://localhost:10001
```

## How to Run Locally

### Complete Step-by-Step Setup

#### Step 1: Get Your Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key or use an existing one
3. Copy the API key - you'll need it for the next steps

#### Step 2: Configure Environment Variables
1. In the main project directory (`purchasing-concierge-a2a/`), edit the `.env` file:
   ```bash
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=your_actual_gemini_api_key_here
   PIZZA_SELLER_AGENT_URL=http://localhost:10000
   BURGER_SELLER_AGENT_URL=http://localhost:10001
   ```

2. The agent `.env` files are already configured, but ensure they have your API key:
    - `remote_seller_agents/pizza_agent/.env` (uses `GOOGLE_API_KEY`)
    - `remote_seller_agents/burger_agent/.env` (uses `GEMINI_API_KEY`)

#### Step 3: Start the Burger Agent
Open **Terminal 1** and run:
```bash
cd purchasing-concierge-a2a/remote_seller_agents/burger_agent
uv sync --frozen
uv run .
```
**Expected output**: Server starts on `http://localhost:10001`
```
INFO: Started server process [XXXX]
INFO: Uvicorn running on http://0.0.0.0:10001 (Press CTRL+C to quit)
```

#### Step 4: Start the Pizza Agent
Open **Terminal 2** and run:
```bash
cd purchasing-concierge-a2a/remote_seller_agents/pizza_agent
uv sync --frozen
uv run .
```
**Expected output**: Server starts on `http://localhost:10000`
```
INFO: Started server process [XXXX]
INFO: Uvicorn running on http://0.0.0.0:10000 (Press CTRL+C to quit)
```

#### Step 5: Start the Purchasing Concierge Web Interface
Open **Terminal 3** and run:
```bash
cd purchasing-concierge-a2a/purchasing_concierge
uv sync --frozen
cd ..  # Return to root directory
source .venv/bin/activate
uv run adk web
```
**Expected output**: Web server starts (usually on `http://localhost:8000`)
```
INFO: Started server process [XXXX]
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Important**: The `adk web` command must be run from the root project directory (`purchasing-concierge-a2a/`) where the agent files are located, not from the `purchasing_concierge/` subdirectory.

#### Step 6: Test the System
1. Open your web browser and go to `http://localhost:8000` (or the URL shown in Terminal 3)
2. You should see the Google ADK web interface
3. Try sending messages like:
   - "I want to order a classic cheeseburger"
   - "Show me the pizza menu and prices"
   - "I'd like a pepperoni pizza and a spicy chicken burger"

The concierge agent will automatically communicate with the appropriate seller agents and coordinate your order.

## Testing the System

1. Ensure all three agents are running (burger, pizza, and concierge)
2. Open the web interface (usually at `http://localhost:8000` or similar)
3. Try queries like:
   - "I want to order a classic cheeseburger"
   - "Show me the pizza menu"
   - "I'd like a pepperoni pizza and a spicy chicken burger"

The concierge agent will delegate to the appropriate seller agents based on your request.

## Architecture

- **Purchasing Concierge Agent**: Main orchestrator using Google ADK with Gemini API
- **Pizza Agent**: Specialized agent using LangGraph and Gemini API
- **Burger Agent**: Specialized agent using CrewAI and Gemini API
- **Communication**: All agents communicate via A2A protocol over HTTP

## Troubleshooting

### Common Issues

1. **"Module not found" errors**: Ensure you've run `uv sync --frozen` in each agent directory
2. **API key errors**: Verify your Gemini API key is correctly set in all `.env` files
3. **Port conflicts**: Ensure ports 10000, 10001, and 8000 are available
4. **Connection errors**: Make sure all agents are running before testing

### Agent Logs

Each agent will display logs in its terminal. Check for any error messages or connection issues.

## Key Differences from Cloud Version

- **No Google Cloud Project required**: Runs entirely locally
- **No Vertex AI deployment**: Uses Gemini API instead
- **Simplified setup**: No gcloud authentication or API enabling needed
- **Local networking**: Agents communicate via localhost URLs

## Next Steps

- Explore the agent code to understand the A2A protocol implementation
- Modify agent behaviors or add new seller agents
- Experiment with different Gemini models
- Learn about LangGraph and CrewAI frameworks used

---

For the original cloud deployment version, see the main README.md file.