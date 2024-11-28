# Teagardan: Your Multi-Agent AI System

Teagardan: Your Local Multi-Agent AI System

Introducing a local task management with a powerful, flexible, and extensible AI framework.

Teagardan is a multi-agent AI system designed for efficient and adaptable handling of tasks on your local machine. Built from the ground up for scalability and extensibility, Teagardan empowers you to manage complex workflows with ease, without relying on external servers or cloud services.  It leverages a modular agent system, allowing you to create diverse AI agents, each with specialized skills and tools, working together to accomplish complex tasks locally. Teagardan intelligently assigns tasks to the best-suited agents based on their skills and the task requirements, optimizing efficiency and performance. A variety of tools, including web search, web scraping, and local file system access, empower agents to gather and process information from diverse sources. Teagardan also incorporates a local knowledge graph (using Neo4j) and a memory manager for context-aware task processing and supports user authentication and management for secure access and collaboration within your local environment.


## Features

* **Modular Agent System:** Define and manage agents with specific skills, tools, roles, and permissions.  Agents can be dynamically created, updated, and terminated through the UI.
* **Dynamic LLM Loading:** Efficiently load and unload LLMs on demand, supporting different model types (e.g., llama.cpp, Hugging Face Transformers).  Model selection and configuration are managed through the System Administration UI.
* **Tool Integration:** Easily integrate custom tools (web search, web scraping, file system access, etc.).  Includes a `ToolManager` for registering and accessing tools, and a plugin system for adding new tools.
* **Task Management:**  Create, queue, assign, prioritize, execute, and track tasks with dependencies.  The Task Manager UI provides an intuitive interface for managing complex workflows.
* **Memory Management:** Store and retrieve information using embeddings and a knowledge graph. Supports context window management for efficient handling of large contexts.
* **Knowledge Graph Integration:** Integrate a knowledge graph (using Neo4j) to represent and reason over structured knowledge. The Knowledge Graph Visualization UI allows users to explore and interact with the graph.
* **User Authentication and Management:** Secure access to the framework with user authentication, role-based permissions, and user profile management.
* **Flexible Prompt Management:** Use prompt templates or construct prompts dynamically for different task types, enabling advanced prompting techniques like chain-of-thought and few-shot learning.
* **Comprehensive Error Handling and Logging:** Robust error handling and detailed logging throughout the framework, improving debuggability and maintainability.
* **Metrics Tracking:** Track task performance, agent efficiency, and other key metrics to monitor system performance and identify areas for optimization.  Metrics are visualized in the UI.
* **React-based User Interface:** Manage agents, tasks, the knowledge graph, user profiles, and system settings through an intuitive and customizable web interface.


## Installation

### Prerequisites

* **Git:** For version control.
* **Python 3.11+:**  With the following packages (managed using `pip` and `requirements.txt`):  `flask`, `sqlite3`, `llama-cpp`, `requests`, `sentence-transformers`, `neo4j`, `python-dotenv`, `PyJWT`, `transformers`.  It is recommended to use a virtual environment for this. 
* **Node.js and npm:** For the frontend (React app).
* **LLM Model (e.g., GGML/GGUF):** Download and place your chosen LLM model in the `backend/models` directory (or configure the `MODELS_DIR` in `backend/utils/config.json`). If the directory does not exist, you may create it manually or during setup. Instructions on installing and running `ollama` are below.  You can also place them elsewhere and update the config accordingly.
* **Neo4j (for Knowledge Graph):** Install and run Neo4j. Instructions can be found in the Neo4j documentation.

### Setting up

1. **Clone the Repository:**

   ```bash
   git clone <your_repo_url>  #Replace with your github URL
   cd teagardan
Use code with caution.
Markdown
Backend Setup:
Set up and activate a Python virtual environment (highly recommended):
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
Use code with caution.
Bash
*Install dependencies:
pip install -r backend/requirements.txt
Use code with caution.
Bash
Configure API keys, database credentials, model paths, and other settings in backend/utils/config.json. See backend/utils/config.example.json for an example. Create your config.json, ensuring all necessary values are present.
Make sure to create the models directory if it does not exist and add your LLM model there.
Frontend Setup:
cd frontend
npm install
Use code with caution.
Bash
Neo4j Setup (for Knowledge Graph):
Install and start Neo4j.
Create a database and user credentials as described in the Neo4j documentation.
Ensure the connection details in backend/utils/config.json are correct.
Ollama Setup:
Installation: Install Ollama by following instructions on their official site at https://ollama.ai. Ollama has different installation methods and versions based on operating system and hardware architecture, so select the appropriate one. It is highly recommended to follow their instructions as they often update. For example, if installing on a Mac with Apple Silicon, go to https://ollama.ai/download and under the Apple Silicon tab, run /bin/bash -c "$(curl -fsSL https://ollama.ai/install.sh)". If you are installing on another operating system, follow the relevant instructions from the Downloads page.
Downloading and Running Models: You can use the Ollama CLI to download models and start the Ollama server. For example, to download the llama3.2 model, run ollama pull llama3.2. After installing and starting ollama, you may leave the server running and make requests to it as needed. Refer to the documentation on https://ollama.ai for specific commands and usages, including how to start servers, modify parameters and settings, or run specific models.
Model Placement and Configuration: Place your .gguf model files in the models directory, or configure the MODELS_DIR variable in your backend config (backend/utils/config.json) to specify the correct location if your models are stored somewhere else. Update the model paths in api.py or other relevant files as needed, so that the server knows where to find your models. This can be done by making requests to the running ollama server, or directly referencing models from local file system using llama.cpp.
Running the Application
Start the Backend:
cd backend
python api.py  # Or flask run, or other methods.  Ensure necessary environment variables are set.
Use code with caution.
Bash
Start the Frontend (Optional):
cd frontend
npm start
Use code with caution.
Bash
The React app will typically run on http://localhost:3000 (or the port specified in your Webpack config).
Example Use Case
See the earlier README example; the use case and workflow should remain unchanged. It is generally a good idea to use real examples, rather than placeholders to ensure that your application works as intended. This may also help discover areas of improvement for tools, prompt engineering, agents, or other functionalities. You can also update and add more use cases if needed, to further demonstrate the capabilities and uses of the Teagardan framework.

Testing
Backend Tests
Ensure you have a test database or setup a Neo4j test instance and add test data to it if necessary. For example, set up a new user, agent, etc. If you are using a local database and it is not being tracked via .gitignore, then consider backing it up, as running tests may modify or clear the database. Ensure that all necessary environment variables are correctly set for database connections and external APIs.
Navigate to the project root directory.
Activate your virtual environment.
Install test dependencies (if you use a requirements-test.txt file).
Run tests with pytest:
pytest backend  # Add any pytest arguments or flags as needed (coverage reporting, etc.)
Use code with caution.
Bash
For more details or specifications, include a tests section in the README.

Contributing
If you'd like to contribute, follow these steps:

Fork the repository.
Create your feature branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a pull request.
License
This project is licensed under the MIT License.

**Key improvements from the previous README:**

*   **Conciseness and Clarity:** More direct and to-the-point language.
* **Focus on Key Features and Benefits:** Highlights the core strengths and value proposition of Teagardan.
* **Detailed Installation and Setup:** Clearer instructions with separate backend and frontend steps, including activating the virtual environment, configuring `config.json`, and setting up Neo4j, and Ollama, as well as indicating where to store models, or specifying model directory in config files.
* **Frontend URL:** Updated placeholder URL in Usage with actual location (`http://localhost:3000`). Add your actual frontend development server URL here.
* **API and Contributing Placeholders:** Include actual content or remove these sections for now.
* **Ollama section added**: Added Ollama download and setup instructions, and configuration and model placement and running information.
* **Other**: Added testing information for the backend tests, including installing dependencies from a test requirements file, making sure a test database is set up and configured correctly, with environment variables, and including optional instructions on how to add test data. Added contributing section, if this is a concern.
* **Updated License**: Changed License to MIT to match your package.json

This README is more comprehensive and informative, providing a better overview and clear instructions for all phases. Remember to replace placeholder content (URLs, API documentation, contributing guidelines) with your actual information. It's good practice to include usage examples and specific backend API documentation within your README so that others, or yourself when re-visiting this project later, have a clear understanding of how to use and install your application. If you have other information to include, such as acknowledgements, or references, these can also be added as separate sections or added to existing sections, to create a more helpful and comprehensive guide.
Use code with caution.
