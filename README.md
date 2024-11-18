Teagardan: Your Multi-Agent AI System
Revolutionizing task management with a powerful, flexible, and extensible AI framework.

Teagardan is a multi-agent AI system designed for efficient and adaptable task handling. Built from the ground up for scalability and extensibility, Teagardan empowers you to manage complex workflows with ease. It leverages a modular agent system, allowing for the seamless integration of diverse AI agents, each equipped with specialized skills and tools, working together to accomplish complex tasks. Teagardan intelligently assigns tasks to the best-suited agents, optimizing efficiency and performance. A variety of tools, including web search, web scraping, and local file system access, empower agents to gather and process information from diverse sources. 

Phase 1: Building the Foundation

This initial phase establishes the core components of the Teagardan framework. A robust local LLM interface is implemented for efficient prompt construction, response parsing, and context management. A flexible agent system handles registration, communication, lifecycle management, and validation. A diverse set of basic tools supports web searching, web content extraction, and local file system operations. A scalable task manager facilitates task definition, allocation, execution, completion, and performance metrics tracking. Finally, a foundational memory manager enables hybrid retrieval, dynamic knowledge updates, and enhanced semantic search capabilities.

Future Development (Phase 2 and Beyond)

Future phases will significantly expand Teagardan's capabilities. 

Join the Teagardan Community!

## Getting Started

This guide helps you set up and run the Teagardan project.

**Prerequisites:**

*   Git
*   Python 3.11 (or later)  with the following packages: `flask`, `sqlite3`, `llama-cpp`, `requests`, `sentence-transformers` (see `requirements.txt` for a complete list).
*   Node.js and npm (for the frontend)
*   An LLM model (e.g., a GGML model in `.gguf` format) for local use.  Place this model in a directory specified in `api.py`.  You may have to make a directory for your model files.
*   Ollama (if you want to use ollama models)


**Steps:**

1.  **Clone the Repository:** `git clone <your_repo_url>`

2.  **Create the Database:** Create a SQLite database file named `agent_data.db` in the `masterplan` directory.  (The database is created automatically if it does not exist, when the server starts, but you might want to pre-create one if needed.)

3.  **Install Python Dependencies:** Navigate to the `masterplan` directory and run: `pip install -r requirements.txt` (This assumes you have a `requirements.txt` file listing all required Python packages.)

4.  **Install Frontend Dependencies:** Navigate to the `masterplan/agent-system` directory and run: `npm install`

5.  **Configure the LLM:** Update the `model_path` variable in `masterplan/api.py` to point to your local LLM model file. For example:  `model_path = "/path/to/your/llama-model.gguf"`

6.  **Run the Flask Server:** Navigate to the `masterplan` directory and run: `python api.py` (This starts the Flask web server on the specified port. Check for the `port` variable in `api.py`)

7.  **Start the React Development Server (Optional, for web UI):** If you are using the React application, navigate to the `masterplan/agent-system` directory and run `npm start`. This will start a development server and open the application in your browser (usually on port 8080).


8.  **Access the UI:** Open your web browser and navigate to the URL specified by your Flask or React development server.  The URL will usually be `localhost` for the React UI and  `localhost' for API access.

Example Use Case: iPhone 14 Pro Web Search

User Interaction: A user interacts with the Teagardan system (through a UI, CLI, or API call), providing the following query: "What are the key features of the iPhone 14 Pro?"
Agent Selection: The AgentSystem receives the query. Based on its task assignment logic (keyword matching or other criteria), it selects the agent best equipped to handle web searches (let's assume this agent is named "WebSearcher").
Agent Action: The selected agent ("WebSearcher") receives the query. Because the query contains keywords related to web searching, the "WebSearcher" agent uses its WebSearchTool to perform a Google Custom Search API request.
Tool Execution: The WebSearchTool uses the provided query and the Google Custom Search Engine ID to query Google's Custom Search JSON API. It receives the JSON response containing the search results.
Response Processing: The WebSearchTool processes the JSON response, extracting relevant information (titles, URLs, snippets) from the top search results. It formats the extracted information into a human-readable string.
Agent Response: The "WebSearcher" agent sends the formatted string containing the search results back to the AgentSystem.
System Output: The AgentSystem displays this information to the user, potentially adding it to the conversation history and updating the context in the MemoryManager. The response might look like this:
Here's what I found about the key features of the iPhone 14 Pro:

Title: iPhone 14 Pro - Apple
URL: https://www.apple.com/iphone-14-pro
Description:  The iPhone 14 Pro features a stunning Super Retina XDR display with ProMotion, an advanced A16 Bionic chip, and a revolutionary 48MP Main camera.  It also includes innovative safety features like Emergency SOS via satellite.

Title: iPhone 14 Pro Review: A Near-Perfect Phone
URL: https://www.example.com/iphone-14-pro-review
Description:  A detailed review highlighting the iPhone 14 Pro's performance, camera capabilities, and battery life.
Use code with caution.
Context Update: The MemoryManager updates its context, storing the user's query and the search results for future use (in case the user asks related questions).


For more advanced setup, usage instructions, and details on contributing, please refer to the documentation.

Teagardan is an open-source project, fostering community collaboration. Contribute to this exciting project, help shape the future of AI-powered task management, and transform how you work!

License: Apache License 2.0
