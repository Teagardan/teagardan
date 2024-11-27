# Teagardan: An AI Agent Framework

Teagardan is a flexible and extensible framework for building and managing AI agents that interact with LLMs (Large Language Models), tools, and a knowledge graph.  It provides a modular architecture, making it easy to customize and extend with new agent types, tools, and functionalities.

## Features

* **Modular Agent System:** Define and manage agents with specific skills, tools, roles, and permissions.
* **Dynamic LLM Loading:**  Efficiently load and unload LLMs on demand, supporting different model types (e.g., llama.cpp, Hugging Face Transformers).
* **Tool Integration:**  Easily integrate custom tools for web search, information extraction, file system access, and more.  Includes a `ToolManager` for registering and accessing tools.
* **Task Management:** Create, queue, assign, execute, and track tasks with priorities and dependencies.
* **Memory Management:** Store and retrieve information using embeddings and a knowledge graph. Supports context window management.
* **Knowledge Graph Integration:**  Integrate a knowledge graph (using Neo4j) to represent and reason over structured knowledge. (See Phase 3 implementation)
* **User Authentication and Management:**  Secure access to the framework with user authentication and role-based permissions.
* **Flexible Prompt Management:** Use prompt templates or construct prompts dynamically for different task types.
* **Comprehensive Error Handling and Logging:** Robust error handling and detailed logging throughout the framework.
* **Metrics Tracking:**  Track task performance, agent efficiency, and other key metrics.
* **React-based User Interface:**  Manage agents, tasks, and the knowledge graph through an intuitive web interface. (Frontend implementation)

## Installation
replace this _ACTUAL_PATH_/llama.cpp/llama-3.2-3b-instruct-q8_0.gguf with your actual location in files as needed. 
### Prerequisites

* Python 3.9+
* Node.js and npm (for frontend)
* Neo4j (for knowledge graph - Phase 3)
* Ollama (for llama.cpp models)
* Install Python dependencies:
```bash
pip install -r backend/requirements.txt 