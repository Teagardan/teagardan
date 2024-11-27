import logging
import time
import uuid
from datetime import datetime
from typing import List, Dict, Any
from queue import PriorityQueue   # For task prioritization

# ... (other imports from agent.py, tool_manager.py, etc. as needed)
logger = logging.getLogger(__name__)


class Task:  # Task data structure
    def __init__(self, task_id, description, agent_id=None, status="pending", priority="medium", created_at=None, metrics=None): # Add priority, creation timestamp, and metric storage.
        self.id = task_id
        self.description = description
        self.agent_id = agent_id  #Make sure it's an integer

        self.status = status
        self.priority = priority
        self.created_at = created_at or datetime.now()  #Store datetime object.

        self.metrics = metrics or {} #Store metrics in dictionary



class TaskManager:
    def __init__(self, agent_system):  #Dependency injection for AgentSystem.
        self.agent_system = agent_system
        self.task_queue = PriorityQueue()  # For handling pending tasks
        self.tasks: Dict[str, Task] = {}  # Dictionary to store tasks by ID
        self.available_agents = set()  # Keep track of agents
        # (Optional) self.db = database_connection  # If using database.


    def create_task(self, description: str, agent_id: int = None, priority: str = "medium") -> str: #Correctly creates task and logs
        """Creates a new task and adds it to the task queue."""
        try:
            task_id = str(uuid.uuid4())  #Generate unique ID
            created_at = datetime.now()  # Get creation timestamp.
            task = Task(task_id, description, agent_id, "pending", priority, created_at) #Correctly creates task object using current datetime.
            self.tasks[task_id] = task  # Add task to dictionary
            self.add_task_to_queue(task) #Add the task to the task queue.
            logger.info(f"TaskManager.create_task: Created task '{description}' with ID '{task_id}'.")  # Logs task creation.
            return task_id  # Return the task ID
        except Exception as e:
            logger.error(f"TaskManager.create_task: Error creating task: {e}")  #Logs error

            return None #Return None on error




    def add_task_to_queue(self, task: Task):
        """Adds a task to the priority queue."""
        priority_mapping = {"high": 0, "medium": 1, "low": 2}  # Higher value = lower priority
        priority = priority_mapping.get(task.priority, 1) # Get priority value. Defaults to medium (1).
        self.task_queue.put((priority, task)) #Put the task in the queue.



    def get_task_from_queue(self) -> Task or None:  # Correct return type
        """Retrieves and removes highest priority tasks from the queue."""
        try:
            if not self.task_queue.empty():
              _, task = self.task_queue.get() # Get and remove highest priority task (tuple - (priority, task)).  Gets the first element, if equal priority.  To prioritize tasks of equal priority based on which was received first, consider using a timestamp in the tuple, so that if two elements have the same priority, then the one with the earlier timestamp will be selected.
              return task
            else:
              return None
        except Exception as e:
            logger.error(f"TaskManager.get_task_from_queue: Error getting task: {e}")  # Log and return None.  Handle any error appropriately, e.g. by returning None, which signals failure to retrieve task.
            return None  # Or raise an exception if needed.




    def assign_task(self, task: Task): #Assigns a task.  Updates Task.agent_id and logs.
        """Assigns a task to the next available agent."""

        if task.status != "pending":  # Only assign pending tasks.
            logger.warning(f"TaskManager.assign_task: Task '{task.id}' is not pending. Current status: {task.status}")  #Provide more details about task.

            return  #Or raise exception

        agent = self.get_available_agent() #Get the next available agent.
        if agent: #Update if agent available, otherwise log warning.

            task.agent_id = agent.id #Assign to the agent.
            task.status = "assigned"  # Correct status change

            logger.info(f"TaskManager.assign_task: Task '{task.description}' assigned to agent '{agent.name}'.")
        else:
            logger.warning(f"TaskManager.assign_task: No available agents to assign task '{task.description}'.")  # No available agents. Provide more details such as the task that could not be assigned.  Can add it back to the queue here, using the add_task_to_queue method from earlier.




    def get_available_agent(self):
        """Gets the next available agent from the agent system.  Can add logic to get agent based on skill or other criteria later."""
        # ... Your logic for getting the next available agent here ...
        # ... For now, this simple implementation just returns the first active agent
        # ... that isn't already working on a task (consider adding skill/task suitability).
        for agent in self.agent_system.agents: #Simplified implementation for now.  No skill or suitability checks.
            if agent.status == "active" and agent.id not in [task.agent_id for task in self.tasks.values() if task.status == 'assigned']: #Checks that an agent is available.
                return agent

        return None


    def execute_task(self, task: Task) -> Any:  # Correct return type hint
        """Executes a task by delegating to assigned agent."""
        if not task.agent_id:
            logger.error(f"TaskManager.execute_task: Task '{task.description}' has no agent assigned.")  # More specific error message
            return None  # Or raise an exception if you prefer


        agent = self.agent_system.get_agent_by_id(task.agent_id) # Get the agent using agent_id.  Make sure get_agent_by_id exists and returns None if not found!
        if not agent: #Handles case if agent not found.
            logger.error(f"TaskManager.execute_task: Agent with ID '{task.agent_id}' not found for task '{task.description}'.")
            return None

        start_time = time.time()
        try:
            task.status = "in_progress"
            result = agent.handle_task(task.description) #Execute the task.  Handle exceptions here!
            task.status = "completed" #Mark as completed.
            end_time = time.time()
            task.metrics['execution_time'] = end_time - start_time  #Store execution time

            return result #Return result.
        except Exception as e:
            task.status = "failed"
            end_time = time.time()
            task.metrics['execution_time'] = end_time - start_time
            logger.error(f"TaskManager.execute_task: Agent '{agent.name}' failed to execute task '{task.description}': {e}")  # Log agent failure.
            task.metrics['error'] = str(e)  # Save error info

            return None  # Return None to signal task failure.



    def update_task_status(self, task_id: str, status: str):
        """Updates task status."""

        task = self.tasks.get(task_id) #Get task by ID
        if not task: #Make sure it's valid.
            logger.warning(f"TaskManager.update_task_status: Task with ID '{task_id}' not found.")
            return #Or raise an exception


        task.status = status #Update status.  Make sure status is a valid status value.



    def update_task(self, task_id: str, updates: Dict[str, Any]):
      """Updates a task with the provided updates."""

      task = self.tasks.get(task_id) #Retrieve task by id
      if not task:  # Task not found.  Handle the error.

          logger.error(f"TaskManager.update_task: Task with ID '{task_id}' not found.")  # More detail
          return False


      for key, value in updates.items():  # Iterate over the updates provided.
          if hasattr(task, key):  # Only updates attributes that exist in the task object to avoid adding unnecessary properties.

              setattr(task, key, value)  # Update using setattr


      return True



    def delete_task(self, task_id: str) -> bool:  # Type hint added
        """Deletes a task from the task manager."""
        task = self.tasks.get(task_id)

        if not task: # Task not found. Handle appropriately.

            logger.error(f"TaskManager.delete_task: Task with ID '{task_id}' not found.")  # More detailed messages
            return False  # Signal failure


        del self.tasks[task_id] #Remove from the task list.

        # If you're using a separate task queue (not implemented here), remove the task from the queue as well.
        # If you are persisting tasks (e.g. using a database), add deletion there as well.  Implement this logic later!

        return True  # Return True to indicate successful deletion




    def get_tasks(self, agent_id=None): #Filters by agent, includes all information.  Returns list of dicts.
        """Returns all tasks, or tasks for a specific agent, if agent_id is provided."""

        try:
            if agent_id: #Filter if agent_id provided.
                tasks = [task for task in self.tasks.values() if task.agent_id == agent_id]
            else:
                tasks = list(self.tasks.values())  #List of Task objects


            # Converts each Task object to a dictionary and includes all relevant info.
            task_list = []
            for task in tasks:
                task_data = {
                    'id': task.id,
                    'description': task.description,
                    'agent_id': task.agent_id,
                    'status': task.status,
                    'priority': task.priority,
                    'created_at': task.created_at.isoformat(), #Format datetime to string to allow returning it, since datetime objects are not JSON-serializable
                    'metrics': task.metrics

                }
                task_list.append(task_data)  #Add task to list of tasks to be returned.

            return task_list  #Returns list of dictionaries, for jsonifying.
        except Exception as e: #Handles any errors that occur during task retrieval or filtering, and returns an empty list as a result.
            logger.error(f"TaskManager.get_tasks:  Error getting tasks: {e}") # Log the error for debugging.

            return [] # Return empty list on error.




# Example usage in your main application loop or API endpoint:
# task_manager = TaskManager(agent_system)  # Pass the agent_system instance
# task_id = task_manager.create_task("Write a poem about nature.", agent_id=1, priority="high")

# # ... (Later, when ready to execute)
# task = task_manager.get_task_from_queue()
# if task:
#     result = task_manager.execute_task(task)

#     if result:
#         # Process successful task result
#         pass 
#     else:  #If the task has failed, for example, no results found, etc.
#         # Handle task failure
#         pass


# Example API endpoints in api.py
# ... (Other imports) ...
# from task_manager import TaskManager, Task
# ...



# @app.route('/tasks', methods=['GET'])  #Example route.
# def get_tasks_route():
#     agent_id = request.args.get("agent_id")  #Get agent ID from query parameters.  If not provided, agent_id is None

#     tasks = task_manager.get_tasks(agent_id=agent_id)  #Retrieve tasks
#     return jsonify(tasks), 200  #Returns all tasks or those filtered by agent ID


# @app.route('/tasks/<task_id>', methods=['DELETE'])
# def delete_task_route(task_id):
#     deleted = task_manager.delete_task(task_id)  #Deletes the task using task manager.


#     if deleted: #If task deletion is successful.

#         return jsonify({"message": "Task deleted"}), 200 #Success
#     else:  # Task not found or another error occurred during deletion.

#         return jsonify({"error": "Task not found or could not be deleted"}), 404  #Not Found.

#Add routes for other functions - add_task, update_task, etc.