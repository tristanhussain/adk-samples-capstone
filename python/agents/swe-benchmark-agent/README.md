# SWE Benchmark Agent

## Overview

This agent is designed to show the basic principles for tackling software engineering problems from two prominent benchmarks: SWE-bench and TerminalBench. It is not meant to be a production ready implementation.

## Agent Details

| Feature | Description |
| --- | --- |
| **Interaction Type** | Autonomous |
| **Complexity**  | Advanced |
| **Agent Type**  | Single Agent |
| **Components**  | Tools: Shell |
| **Vertical**  | Software Engineering |

### Agent architecture:

The SWE Benchmark Agent uses a sophisticated orchestrator pattern:
- **Orchestrator**: Manages the agent lifecycle and coordinates tool execution
- **Environment**: Docker-based isolated execution environment (SWEBenchEnvironment or TerminalBenchEnvironment)
- **Tools**: File operations (read, edit, create), shell commands, and submission
- **Agent**: LLM-powered agent (Gemini) with built-in planner and thinking capabilities

The agent operates autonomously within the Docker environment, using shell commands and file operations to solve software engineering tasks.

## Using Agent Starter Pack (ASP)

The recommended way to set up and run this agent is with the [Agent Starter Pack](https://goo.gle/agent-starter-pack), which provides a production-ready project with automated deployment and CI/CD.

```bash
# Install and scaffold the project using uv (recommended)
uvx agent-starter-pack create my-swe-agent -a adk@swe-benchmark-agent
```

The starter pack will prompt you to select deployment options and provides additional production-ready features including automated CI/CD deployment scripts.

## Quick Start

### 1. Prerequisites

*   **Python 3.10+**
*   **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — fast Python package manager
*   **Google Cloud SDK (`gcloud`)** installed and authenticated
*   **Git**

### 2. Installation

```bash
git clone https://github.com/google/adk-samples.git
cd adk-samples/python/agents/swe-benchmark-agent

# Install all dependencies (including dev tools)
uv sync --dev
```

### 3. Configuration

Set up Google Cloud credentials (or use a `.env` file):

```bash
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=<your-project-id>
export GOOGLE_CLOUD_LOCATION=<your-project-location>
gcloud auth application-default login
```

### 4. Run Tests

```bash
uv run pytest tests
```

---

## Running Evaluations

The SWE Agent can be evaluated on both SWE-bench and TerminalBench benchmarks to measure its performance on real-world software engineering tasks.

### SWE-bench Evaluation

To run evaluation on the full SWE-bench Verified dataset:

```bash
uv run python -m swe_benchmark_agent.main --full-dataset --evaluate --max-workers 4
```

To evaluate on a specific number of instances (e.g., the first 10):

```bash
uv run python -m swe_benchmark_agent.main --instance-id-or-count 10 --evaluate
```

To evaluate on a single instance:

```bash
uv run python -m swe_benchmark_agent.main --instance-id-or-count django__django-12345 --evaluate
```

### TerminalBench Evaluation

To run evaluation on the full TerminalBench core dataset:

```bash
uv run python -m swe_benchmark_agent.main --dataset terminalbench --full-dataset --evaluate --max-workers 4
```

To evaluate on a specific number of tasks (e.g., the first 5):

```bash
uv run python -m swe_benchmark_agent.main --dataset terminalbench --instance-id-or-count 5 --evaluate
```

To evaluate on a single task:

```bash
uv run python -m swe_benchmark_agent.main --dataset terminalbench --instance-id-or-count blind-maze-explorer-5x5 --evaluate
```

## Customization

The SWE Agent can be customized to better suit your requirements. For example:

 1. **Use a different model:** You can change the model used by the agent by modifying the `main.py` file.
 2. **Add more tools:** You can add more tools to the agent to give it more capabilities.
 3. **Support more benchmarks:** You can add support for more benchmarks by creating a new environment and updating the `main.py` file.
