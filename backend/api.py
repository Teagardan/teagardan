from flask import Flask, request, jsonify, make_response, abort
from agent_system import AgentSystem
from llm_interface import LLM_Interface
from memory_manager import MemoryManager
from agent import Agent
from flask_cors import CORS
import sqlite3
import json
import os
from uuid import uuid4  # For generating UUIDs
import logging


# --- Configure logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




app = Flask(__name__)
CORS(app)  # Enable CORS for all routes and origins

# Get the directory of the current script.  Good practice for Flask apps.
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'agent_data.db')

# Move model loading and agent system initialization to app context later:
# For now, keep these outside:
model_path = "_ACTUAL_PATH_/llama.cpp/llama-3.2-3b-instruct-q8_0.gguf"  # Update this path if needed.
llm_interface = LLM_Interface(model_path=model_path)  # Initialize the LLM interface with model path
memory_manager = MemoryManager()
agent_system = AgentSystem(llm_interface, memory_manager)  # Initialize with LLM


# --- Database setup ---
def create_tables():
    with sqlite3.connect(db_path) as conn:  # Proper connection handling
        cursor = conn.cursor()

        #Agents table - add fields for tools, roles, permissions, and status.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                skills TEXT,
                tools TEXT,       --New field for tool access.
                role TEXT,        --New field to store role.
                permissions TEXT,  --New field to store permissions.
                status TEXT       --New field for status (e.g. active/inactive).

            )
        ''')

        # Create other tables as needed...
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                description TEXT NOT NULL,
                agent_id INTEGER,  --Foreign key referencing agents
                status TEXT,
                priority TEXT,  --Task prioritization
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  --Timestamp
            )
        ''')


        cursor.execute('''  --Table to store user accounts.
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,  --Hash passwords!
                role TEXT,
                profile_picture TEXT  --For storing URL or path to profile picture
            )
        ''')


        cursor.execute('''  --Table to store user settings (system administration)
            CREATE TABLE IF NOT EXISTS system_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                selected_model TEXT,      --Store model setting
                api_key TEXT,            --Store API key if applicable
                max_context_window_size INTEGER,  --Store window size
                logging_level TEXT,      --Log level
                database_file_path TEXT,  --DB file
                debug_mode BOOLEAN,     --Store debug mode setting
                feature_enabled BOOLEAN  --Other features you add
            )
        ''')
        cursor.execute('''  --Messages table to store message history for each agent.
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                agent_id INTEGER,        --Agent's ID.
                text TEXT NOT NULL,      --The message content
                sender TEXT NOT NULL,    --'user' or 'agent' (or agent name).
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')


        conn.commit()

create_tables()



# --- Agent routes ---
@app.route('/agents', methods=['GET'])
def get_agents():
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row  # Access columns by name
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM agents")
            agent_rows = cursor.fetchall()

        # Convert to dictionaries for JSON response
        agents = [dict(row) for row in agent_rows]  # Convert rows to dictionaries. Handles any data type appropriately.
        return jsonify(agents), 200  

    except sqlite3.Error as e:
        logger.error(f"get_agents: Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        logger.error(f"get_agents: An unexpected error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/agents', methods=['POST'])
def create_agent():
    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        skills = data.get('skills')
        tools = json.dumps(data.get('tools', []))      # Tools as JSON string
        role = data.get('role')                           #Get agent role
        permissions = json.dumps(data.get('permissions', {})) # Permissions as JSON, default empty dict
        status = data.get('status', 'inactive')             #Agent status, default 'inactive'

        if not name:
            return jsonify({'error': 'Agent name is required'}), 400


        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''  --Insert skills as JSON string into the database.
                    INSERT INTO agents (name, description, skills, tools, role, permissions, status) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (name, description, json.dumps(skills), tools, role, permissions, status)
                )
                conn.commit()
                new_agent_id = cursor.lastrowid
            except sqlite3.IntegrityError as e:
                conn.rollback()
                return jsonify({'error': str(e)}), 409  #409 CONFLICT if agent name already exists.  Return more details about error for debugging purposes.  
            
        # Return new agent ID
        return jsonify({'message': 'Agent created', 'id': new_agent_id}), 201  

    except sqlite3.Error as e:
        logger.error(f"create_agent: Database error: {e}")
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        logger.error(f"create_agent: An unexpected error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route('/agents/<int:agent_id>', methods=['PUT'])  # PUT method for updates
def update_agent(agent_id):
    try:
        agent = request.get_json()
        # ... Validation here to check what fields to update (name, desc, skills, tools, role, permissions, etc.).  Update database accordingly.
        # This example only updates status, if present:
        status = agent.get('status')
        if status:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE agents SET status = ? WHERE id = ?", (status, agent_id))
                conn.commit()
        return jsonify({'message': 'Agent updated'}), 200  # OK

    except Exception as e:  # Very broad exception handling for now.  Improve.
        logger.error(f"update_agent: Error updating agent {agent_id}: {e}")  # Log error
        return jsonify({"error": "Failed to update agent"}), 500  #Internal Server Error



@app.route('/agents/<int:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
  # (No changes needed from previous improved version)
  pass


@app.route('/agents/reorder', methods=['POST'])
def reorder_agents():
    try:
        data = request.get_json()
        reordered_agent_ids = [agent['id'] for agent in data]  # Assuming frontend sends the new array of agents.

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            for index, agent_id in enumerate(reordered_agent_ids):
                cursor.execute("UPDATE agents SET sort_order = ? WHERE id = ?", (index, agent_id))  # Assumes you have a sort_order field in agents table.
            conn.commit()
        
        return jsonify({"message": "Agents reordered successfully."}), 200

    except sqlite3.Error as e:
        logger.error(f"reorder_agents: Database error: {e}")  # Log error
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        logger.error(f"reorder_agents: An unexpected error occurred: {e}")  # Log error

        return jsonify({"error": f"Internal server error: {e}"}), 500


# --- Task routes ---
@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")
            task_rows = cursor.fetchall()

        tasks = [dict(row) for row in task_rows]
        return jsonify(tasks), 200

    except sqlite3.Error as e:
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500



@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        description = data.get('description')
        agent_id = data.get('agentId')
        status = data.get('status', 'pending')
        priority = data.get('priority', 'medium')  # Task priority
        task_id = str(uuid4())  # Generate UUID on the backend

        if not description:
            return jsonify({'error': 'Task description is required'}), 400

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (id, description, agent_id, status, priority) VALUES (?, ?, ?, ?, ?)
            ''', (task_id, description, agent_id, status, priority))  # Add task ID
            conn.commit()

        return jsonify({'message': 'Task added', 'id': task_id}), 201  #Return ID of new task.

    except sqlite3.Error as e:
        return jsonify({"error": "Database error"}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500



@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        data = request.get_json()

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Update fields based on provided data (example):
            if 'description' in data:
              cursor.execute("UPDATE tasks SET description = ? WHERE id = ?", (data['description'], task_id))
            if 'agent_id' in data:
              cursor.execute("UPDATE tasks SET agent_id = ? WHERE id = ?", (data['agent_id'], task_id))
            if 'status' in data:
                cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (data['status'], task_id))
            # Update other fields...
            conn.commit()
        
        return jsonify({'message': 'Task updated'}), 200

    except Exception as e:
        return jsonify({"error": "Failed to update task"}), 500  #500 Internal Server Error on failure.



@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()

        return jsonify({'message': 'Task deleted'}), 200

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500


@app.route('/tasks/benchmark', methods=['POST'])  # Route for 9.16 - Task Benchmarking
def benchmark_tasks():
    try:
        tasks = request.get_json()
        # ... Add your benchmarking logic using tasks data...
        # For now, just return a dummy response.
        benchmark_results = {  # Example benchmark results. Replace with your actual logic!
            "task_1": {
                "time": "2.3s",
                "accuracy": "95%",
                "resources": "512MB RAM"
            },
            # ... more results
        }
        return jsonify(benchmark_results), 200

    except Exception as e:
        logger.error(f"benchmark_tasks: Error benchmarking tasks: {e}")
        return jsonify({"error": "Failed to benchmark tasks"}), 500


@app.route('/tasks/queue', methods=['POST'])  # Route for 9.17 - Task Queuing
def queue_task():
    try:
        task = request.get_json()  # Get the task to be queued.
        # Implement your queueing logic here...
        # Examples:
        # - Use a queue data structure or library (e.g., Redis queue, RabbitMQ)
        # - Add to a database table that represents a task queue

        # For now, just log the task and return success.
        logger.info(f"queue_task: Task queued: {task}")  # Log the queued task.

        return jsonify({"message": "Task queued successfully."}), 201  # Return the queued task or task ID.


    except Exception as e:
        logger.error(f"queue_task: Error queueing task: {e}")
        return jsonify({"error": "Failed to queue task"}), 500


# --- User and Authentication routes (Add authentication middleware later) ---
# ... Add your user-related routes here for user management, profile, login/logout ...



@app.route('/users', methods=['GET'])
def get_users():
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email, role, profile_picture FROM users") # Don't return passwords!
            user_rows = cursor.fetchall()

        users = [dict(row) for row in user_rows] # Convert each row to dictionary, which can be JSONified.
        return jsonify(users), 200

    except Exception as e:  # Handle database errors. Provide more specific error handling later.
        return jsonify({"error": str(e)}), 500



@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        # ... Input validation (name, email, password, role, etc.) ...
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')  # Hash this before storing!
        role = data.get('role')

        if not name or not email or not password:
            return jsonify({"error": "Name, email, and password are required."}), 400


        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)
                ''', (name, email, password, role)) # You'll hash passwords before storing!
                conn.commit()
                new_user_id = cursor.lastrowid
            except sqlite3.IntegrityError:
                conn.rollback()
                return jsonify({'error': 'User with that email already exists'}), 409

        return jsonify({'id': new_user_id, 'message': 'User created'}), 201  # Return new user's ID.



    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/users/<int:user_id>', methods=['PUT'])  #PUT request for updates.
def update_user(user_id):
    try:
        user = request.get_json()
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            #Example: Update name and email if provided
            if 'name' in user:  
                cursor.execute("UPDATE users SET name = ? WHERE id = ?", (user['name'], user_id))
            if 'email' in user:
                cursor.execute("UPDATE users SET email = ? WHERE id = ?", (user['email'], user_id))

            # ... update other fields as needed ...
            conn.commit()
        return jsonify({'message': 'User updated'}), 200

    except Exception as e: # Handle possible database or other errors
        return jsonify({"error": str(e)}), 500




@app.route('/users/<int:user_id>', methods=['DELETE'])  #Endpoint to delete a user
def delete_user(user_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

        return jsonify({"message": "User deleted"}), 200  # 200 OK or 204 No Content

    except Exception as e: # Handle database or other errors
        return jsonify({"error": str(e)}), 500




@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))  # Retrieve using email
            user = cursor.fetchone()

        if user and user['password'] == password:  # Check if user exists and password matches. In real app, HASH passwords!
            # ... generate JWT or other token here ... (using a library like Flask-JWT-Extended)
            token = "your_generated_jwt"  # Replace with real token generation.
            return jsonify({"token": token, "user": {  # Don't include password in response!
                "id": user['id'],
                "name": user['name'],
                "email": user['email'],
                "role": user['role'],  # Include other user information
                "profilePicture": user['profile_picture'],  # Include profile picture if available.

            }}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401  #Unauthorized

    except Exception as e:  # Handle database or other errors.  Improve this later!
        return jsonify({'error': str(e)}), 500


@app.route('/logout', methods=['POST'])  #Logout route (may not be strictly necessary if using JWTs on frontend).
def logout():
    # ... Revoke token, clear session, etc. (implementation depends on your auth method)...
    # For now, just return success:
    return jsonify({"message": "Logged out successfully"}), 200



# --- System settings routes ---

@app.route('/system_settings', methods=['GET'])
def get_system_settings():
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM system_settings ORDER BY id DESC LIMIT 1")  # Get most recent settings.
            settings_row = cursor.fetchone()

        if settings_row:
            settings = dict(settings_row)  #Convert row to dictionary to correctly return all values.

            # Convert boolean values to JSON-serializable format if using SQLite.
            for key in ['debug_mode', 'feature_enabled']: # Add other boolean fields.  
              if key in settings:
                settings[key] = bool(settings[key])
            return jsonify(settings), 200
        else:  #Return default values if no settings exist in the database yet.
            default_settings = {
                "selected_model": "default_model_name",
                "api_key": "",
                "max_context_window_size": 2048,  # Example values
                "logging_level": "info",
                "database_file_path": "agent_data.db",
                "debug_mode": False,
                "feature_enabled": True
            }
            return jsonify(default_settings), 200

    except Exception as e:  #Handle error during settings retrieval
        logger.error(f"get_system_settings: Error getting system settings: {e}")
        return jsonify({"error": "Failed to retrieve system settings"}), 500



@app.route('/system_settings', methods=['PUT'])
def update_system_settings():
    try:
        settings = request.get_json()  #Get the updated settings from the request body

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Using parameterized query to prevent SQL injection:
            cursor.execute('''
                INSERT INTO system_settings (selected_model, api_key, max_context_window_size, logging_level, database_file_path, debug_mode, feature_enabled)  -- Other settings
                VALUES (?, ?, ?, ?, ?, ?, ?)  --Other settings
            ''', (
                settings.get("selectedModel"), settings.get("apiKey"), settings.get("maxContextWindowSize"), 
                settings.get("loggingLevel"), settings.get("databaseFilePath"), settings.get("debugMode"), settings.get("featureEnabled")  # Other settings values
            ))
            conn.commit()
        
        return jsonify({"message": "System settings updated successfully."}), 200  # Return the saved settings if necessary, and status code 200

    except Exception as e:
        logger.error(f"update_system_settings: Error updating settings: {e}") #Log the specific error.

        return jsonify({"error": f"Failed to update system settings: {e}"}), 500  #Internal Server error

# --- Agent task handling route ---

@app.route('/agents/<int:agent_id>/tasks', methods=['GET'])  # Route to fetch tasks for a specific agent.
def get_agent_tasks(agent_id):
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE agent_id = ?", (agent_id,))
            task_rows = cursor.fetchall()

        tasks = [dict(row) for row in task_rows]  # Convert to dictionary for jsonify
        return jsonify(tasks), 200

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
    except Exception as e:
        return jsonify({"error": f"Internal server error: {e}"}), 500


@app.route('/agents/<int:agent_id>/start', methods=['POST'])
def start_agent(agent_id):
    try:
        # ... Your logic to start the agent (e.g., load model, initialize tools) ...
        # This is a placeholder - you'll replace with your actual implementation
        with sqlite3.connect(db_path) as conn:  #Update the status after handling request.
            cursor = conn.cursor()
            cursor.execute("UPDATE agents SET status = ? WHERE id = ?", ('active', agent_id))  #Updating status to active when agent starts
            conn.commit() #Commit changes to agents table.


        return jsonify({"message": f"Agent {agent_id} started successfully"}), 200  #OK


    except Exception as e:
        logger.error(f"start_agent: Error starting agent {agent_id}: {e}")
        return jsonify({"error": f"Failed to start agent {agent_id}"}), 500



@app.route('/agents/<int:agent_id>/stop', methods=['POST'])
def stop_agent(agent_id):
    try:
        # ... (Your agent stopping logic.  Unload model, free resources, etc.)

        with sqlite3.connect(db_path) as conn:  #Update the agent's status in the database after the stop request has been handled.
            cursor = conn.cursor()
            cursor.execute("UPDATE agents SET status=? WHERE id=?", ('inactive', agent_id))
            conn.commit()
        return jsonify({"message": f"Agent {agent_id} stopped successfully"}), 200 #Return status code 200, OK

    except Exception as e:
        logger.error(f"stop_agent: Error stopping agent {agent_id}: {e}") #Log the specific error message.

        return jsonify({"error": f"Failed to stop agent {agent_id}"}), 500  #Internal Server Error


@app.route('/task', methods=['POST', 'OPTIONS'])
def handle_task():
    if request.method == 'OPTIONS':  #Handle OPTIONS method for CORS preflight.  Update the headers to only accept values from your origin, rather than all origins, when you go into production.
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response



    try:
        data = request.get_json()
        task_description = data.get('task')
        selected_agent_id = data.get('agent_id')

        # ... (Rest of your task handling logic - no changes needed)
    except Exception as e:
      # ...Handle any exceptions in task processing...
      pass


if __name__ == '__main__':
    # ... (You'll remove the example agent creation here. Agents will be created dynamically via the frontend UI.) ...

    with app.app_context(): # Create app context and load the model now
        llm_interface.load_model()
        # ... create and add any essential, non-dynamic agents here if needed ...
        app.run(debug=True, port=5001)