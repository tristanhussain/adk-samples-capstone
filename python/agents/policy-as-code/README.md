# Policy-as-Code Agent

A generative AI-powered agent designed to automate data governance on Google Cloud. It allows users to define, validate, and enforce data policies using natural language queries, translating them into executable code that runs against **Google Cloud Dataplex** and **BigQuery** metadata.

## Using Agent Starter Pack (ASP)

The recommended way to set up and run this agent is with the [Agent Starter Pack](https://goo.gle/agent-starter-pack), which provides a production-ready project with automated deployment and CI/CD.

```bash
# Install and scaffold the project using uv (recommended)
uvx agent-starter-pack create my-policy-as-code -a adk@policy-as-code
```

The starter pack will prompt you to select deployment options and provides additional production-ready features including automated CI/CD deployment scripts.

## Quick Start

### 1. Prerequisites

*   **Python 3.11+**
*   **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — fast Python package manager
*   **Google Cloud SDK (`gcloud`)** installed and authenticated
*   **Git**

### 2. Installation

```bash
git clone https://github.com/google/adk-samples.git
cd adk-samples/python/agents/policy-as-code

# Install all dependencies (including dev tools)
uv sync --dev
```

### 3. Configuration

1.  Copy the example configuration file:
    ```bash
    cp .env.example .env
    ```

2.  Open `.env` and fill in your details:
    *   `GOOGLE_CLOUD_PROJECT`: Your Google Cloud Project ID.
    *   `GOOGLE_CLOUD_LOCATION`: (e.g., `us-central1`).
    *   `ENABLE_MEMORY_BANK`: Set to `True` to enable long-term memory (requires Firestore). Set to `False` to run without it. See [Memory Integration](./docs/MEMORY_INTEGRATION.md) for details.
    *   `FIRESTORE_DATABASE`: (Optional) Leave as `(default)` unless using a named database.

3.  Authenticate with Google Cloud:
    ```bash
    gcloud auth application-default login
    ```

### 4. Run the Agent

```bash
uv run adk web
```

**Optional:** To enable short-term contextual memory (Agent Engine) for better conversation history:

```bash
uv run adk web --memory_service_uri="agentengine://AGENT_ENGINE_ID"
```

This will start a local web server. Open the URL in your browser to chat with the agent.

### 5. Run Tests

```bash
uv run pytest
```

---

## Key Features

*   **Natural Language Policies**: "All tables in the finance dataset must have a description."
*   **Hybrid Execution**: Generates Python code on-the-fly for flexibility, but executes it in a sandboxed environment for safety.
*   **Memory & Learning**: Uses **Firestore** and **Vector Search** to remember valid policies. If you ask a similar question later, it reuses the proven code instead of regenerating it.
*   **Dual-Mode Operation**:
    *   **Live Mode**: Queries the **Dataplex Universal Catalog** in real-time.
    *   **Offline Mode**: Analyzes metadata exports stored in **Google Cloud Storage (GCS)**.
*   **Compliance Scorecards**: Run a full health check on your data assets with a single command.
*   **Remediation**: Can suggest specific fixes for identified violations.

## Architecture

The agent is built using the **Google Cloud Agent Development Kit (ADK)** and leverages several Google Cloud services:

*   **Gemini 2.5 Pro**: For complex code generation (converting natural language to Python).
*   **Gemini 2.5 Flash**: For conversational logic, tool selection, and remediation suggestions.
*   **Vertex AI Vector Search**: For semantic retrieval of past policies.
*   **Firestore**: Stores policy definitions, versions, and execution history.
*   **Dataplex API**: For fetching live metadata.

### Project Structure

*   `policy_as_code_agent/`
    *   `agent.py`: Entry point and core agent definition.
    *   `memory.py`: Handles Firestore interactions (saving/retrieving policies).
    *   `utils/`: Utility modules for LLM logic, Dataplex, GCS, and common tools.
    *   `simulation.py`: Sandboxed execution engine for running policy code.
    *   `prompts/`: Markdown templates for LLM instructions.
*   `tests/`: Unit and integration tests.
*   `data/`: Sample metadata for local testing.

<details>
<summary><strong>Manual Setup (without ASP)</strong></summary>

### Installation

```bash
git clone https://github.com/google/adk-samples.git
cd adk-samples/python/agents/policy-as-code
uv sync --dev
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, etc.
gcloud auth application-default login
```

### Run the Agent

```bash
uv run adk web
```

### Run Tests

```bash
uv run pytest
```

</details>

## Documentation

For deep dives into the implementation, check the `docs/` folder:
- [High-Level Architecture](./docs/HIGH_LEVEL_DETAILS.md)
- [Low-Level Implementation](./docs/LOW_LEVEL_DETAILS.md)
- [Memory Implementation](./docs/MEMORY_IMPLEMENTATION.md)
