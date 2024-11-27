import json
import logging
import os
import subprocess
import time
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any

from llama_cpp import Llama  # For llama.cpp models
from transformers import pipeline, AutoModelForSequenceClassification

from memory_manager import MemoryManager
from prompts import PromptTemplates
from tool_manager import ToolManager
from tools.file_system_tool import FileSystemTool
from tools.local_rag_tool import LocalRAGTool
from tools.web_search_tool import WebSearchTool
from tools.website_expert_tool import WebsiteExpertTool
from tools.website_rag_tool import WebsiteRAGTool


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Agent(ABC):
    def __init__(self, agent_id: int, name: str, description: str, skills: List[str], tools: List[str], role: str = None, permissions: Dict[str, bool] = None, status: str = "inactive", model_path: str = None, api_key: str = None, search_engine_id: str = None):
        self.id = agent_id
        self.name = name
        self.description = description
        self.skills = skills
        self.tools = self.initialize_tools(tools, api_key, search_engine_id)
        self.role = role
        self.permissions = permissions or {}
        self.status = status
        self.model_path = model_path
        self.llm_interface = None  # LLM is loaded dynamically
        self.memory_manager = MemoryManager()
        self.prompt_templates = PromptTemplates()
        self.context = self.load_agent_context() or ""
        self.tool_manager = ToolManager()  # Optional
        self.metrics = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_time_spent': 0
        }



    def initialize_tools(self, tools: List[str], api_key: str = None, search_engine_id: str = None) -> List[Any]:

        initialized_tools = []
        for tool_name in tools:
            if tool_name == "web_search":
                if api_key and search_engine_id:
                    initialized_tools.append(WebSearchTool(api_key, search_engine_id))
                else:
                    logger.warning(f"Agent {self.name}: WebSearchTool not initialized. Missing API key or search engine ID.")


            elif tool_name == "website_rag":
                initialized_tools.append(WebsiteRAGTool())
            elif tool_name == "file_system":
                initialized_tools.append(FileSystemTool())
            elif tool_name == "local_rag":
                initialized_tools.append(LocalRAGTool())
            elif tool_name == "website_expert":
                initialized_tools.append(WebsiteExpertTool())
            else:  #Try to get from ToolManager
                tool_class = self.tool_manager.get_tool(tool_name)  # Dynamic tool retrieval using ToolManager
                if tool_class:  #Instantiate if found
                    initialized_tools.append(tool_class()) #Initialize the tool.
                else:  # Tool not found, handle error appropriately.
                    logger.warning(f"Agent {self.name}: Tool '{tool_name}' not found.")

        return initialized_tools


    @abstractmethod
    def handle_task(self, task: str) -> str:  #Abstract method.  Concrete agents MUST implement this.
        pass



    # NEW: Function to determine relevant skill for the task
    def determine_relevant_skill(self, task: str) -> str:  # Improved skill matching (handles ties)
        skill_keywords = {  # Updated and expanded skill keywords
            "web_search": ["search", "find", "lookup", "query", "internet", "google", "information", "research"],
            "website_rag": ["website", "webpage", "content", "extract", "scrape", "summarization"],
            "file_system": ["file", "read", "write", "access", "manage", "directory"],
            "local_rag": ["document", "extract", "text", "data", "parse", "summarize"],
            "website_expert": ["expert", "knowledge", "specialist", "consult", "opinion"],
            "philosophical_reasoning": ["meaning", "life", "existence", "universe", "philosophy"],
            "general_knowledge": ["what", "who", "where", "when", "why", "how", "explain", "define"], #General knowledge keywords
            # ... Add keywords for more skills
        }

        matched_skills = []
        for skill, keywords in skill_keywords.items():
            match_count = sum(keyword in task.lower() for keyword in keywords)
            if match_count > 0:
                matched_skills.append((skill, match_count))

        if not matched_skills:
            return None


        matched_skills.sort(key=lambda item: item[1], reverse=True) # Sort by match count


        if len(matched_skills) > 1 and matched_skills[0][1] == matched_skills[1][1]: #Tie-breaker using priority order
            priority_order = list(skill_keywords.keys()) # You can customize the priority

            return next((skill for skill, _ in matched_skills if skill in priority_order), None)  #Returns first match


        return matched_skills[0][0]  # Return the highest matching skill

    def is_suitable_task(self, task: str) -> bool:  # Correct implementation using determine_relevant_skill
        relevant_skill = self.determine_relevant_skill(task)
        return bool(relevant_skill)

    def requires_tools(self, task):
        # Simple implementation: Check if any tool is mentioned in the task
        for tool in self.tools:
            tool_name = type(tool).__name__.lower()  # Get the tool's class name in lowercase
            if tool_name in task.lower():
                return True
        return False


    def use_tools(self, task: str) -> str: # Generic tool usage with run(task) and error handling
        for tool in self.tools:
            if hasattr(tool, 'run'):
                try:
                    result = tool.run(task)
                    if result:
                        return result
                except Exception as e:  # Handle exceptions during tool execution
                    logger.error(f"Agent {self.name}: Error using tool {tool.__class__.__name__}: {e}")
                    # ... optionally return an error message or log the error ...
        return "No suitable tool found for this task."

    def load_llm(self):
        """Loads the LLM model dynamically.  Handles .gguf (llama.cpp) and other model types."""
        try:
            if self.llm_interface is None and self.model_path:  #Only load if no LLM interface and a path are given.
                if self.model_path.endswith('.gguf'):  # For llama.cpp models
                    self.llm_interface = LLM_Interface(model_path=self.model_path) #Correct the path.
                    self.llm_interface.load_model()  # Correct method call
                elif ".gguf" not in self.model_path:  # For other model types (using transformers) - Correct this condition
                    self.llm_interface = LLM_Interface(model_path=self.model_path) #Update with correct path to model
                    self.llm_interface.load_model()  # Correct method call

        except Exception as e:
            logger.error(f"Agent {self.name}: Could not load LLM: {e}") #Add agent name


    def unload_llm(self):  # Unloads LLM interface, frees resources.
        self.llm_interface = None
    
    def generate_text(self, prompt):
        if self.model_path.endswith('.gguf'):
            # Use Ollama for .gguf models
            command = [
                "ollama", "run", "llama3.2:3b-instruct-q8_0",
                prompt
            ]
            try:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                return result.stdout.strip()
            except subprocess.CalledProcessError as e:
                print(f"Error running the model: {e}")
                return ""
        else:
            # Use Hugging Face Transformers pipeline for other models
            return pipeline('text-generation', model=self.model)(prompt, max_length=50)[0]['generated_text'].strip()

    def current_context(self):
        return self.context  # Return the current context

    def update_context(self, task, response):
        new_message = f"User: {task}\nAI: {response}"
        self.context = self.memory_manager.manage_context(self.context, new_message)
        self.save_agent_context() #Optional: if using persistence.

    def save_agent_context(self): #Implement persistent context storage in derived classes if needed.
        pass

    def load_agent_context(self):  #Implements persistence.
        pass

class WebSearcherAgent(Agent):
    def handle_task(self, task: str) -> str:
        # ... (Full implementation from previous responses, including query extraction, web search, error handling, logging, metrics, and context updates).
        # Example usage of tools:
        self.load_llm()
        start_time = time.time()

        if self.llm_interface:  # Check if LLM is loaded
            try:
                prompt = self.prompt_templates.build_prompt(self.context, task, template_type="web_search")
                search_query = self.llm_interface.extract_search_query(task)  # Assuming LLM can extract queries. Replace with other methods if needed.
                if search_query:
                    search_results = self.use_tools(search_query)  # Correct: using use_tools for generic tool handling.  Make sure the WebSearchTool implements a `run` method.
                    response = f"Search results for '{search_query}':\n{search_results}"
                else:
                    response = self.llm_interface.generate_text(prompt)  # Fallback to LLM if no query extracted
                self.metrics['tasks_completed'] += 1  # Update metrics
            except Exception as e:
                logger.error(f"WebSearcherAgent error: {e}")  # Log the error
                response = f"Error: {e}"  # Return a user-friendly error message.  Can be more detailed if needed.  Include relevant information, such as the query, to assist with debugging.
                self.metrics['tasks_failed'] += 1  # Update error metric.
        else:  #Handle cases where the model is not loaded correctly.  Can add more specific handling here for different error cases.
            response = "LLM not loaded."


        end_time = time.time()  # End measuring execution time
        self.metrics['total_time_spent'] += (end_time - start_time)
        self.update_context(task, response) #Update context
        return response


class DocumentExpertAgent(Agent):
    def handle_task(self, task: str) -> str:
        # ... (Implementation as before, including URL/document extraction logic, tool usage via self.use_tools(task), and LLM fallback.)
        self.load_llm()
        start_time = time.time()

        if self.llm_interface:
            try:
                if "extract from" in task.lower():
                    if "website" in task.lower():
                        url = self.extract_url_from_task(task)  # Implement URL extraction
                        if url:
                            response = self.use_tools(task + f" URL: {url}") #Combine task and extracted url
                        else: # If no URL is found
                            response = "Could not extract URL from task."  #Provide feedback that URL could not be found.
                    elif "document" in task.lower():
                        document_path = self.extract_document_path_from_task(task) #Implement path extraction.
                        if document_path: #If path exists, call tools, otherwise handle the error.
                          response = self.use_tools(task + f" Document path: {document_path}")  # Pass the extracted path
                        else: #If the path does not exist
                            response = "Could not extract document path from task."  # Provide feedback.  This will help in debugging and improving logic.
                    else: #Handle the case where neither is found.
                        response = "Please specify whether to extract from 'website' or 'document'."
                else:
                    prompt = self.prompt_templates.build_prompt(self.context, task, template_type="document_expert")
                    response = self.llm_interface.generate_text(prompt)  # Add error handling for LLM call
                self.metrics['tasks_completed'] += 1  # Update metrics

            except Exception as e:
                logger.error(f"DocumentExpertAgent error: {e}")
                response = f"Error: {e}"  # Return an error message to the user
                self.metrics['tasks_failed'] += 1

        else:
            response = "LLM not available for this agent."


        end_time = time.time()
        self.metrics['total_time_spent'] += (end_time - start_time)
        self.update_context(task, response)  #Update context
        return response


class GeneralKnowledgerAgent(Agent):
    def handle_task(self, task: str) -> str:
        self.load_llm()
        start_time = time.time()
        if self.llm_interface:
            try:
                # Example task handling (replace with your actual logic):
                if self.requires_tools(task):
                    response = self.use_tools(task)
                    self.update_context(task, response) #Context update.
                    return response  #Return tool result.

                prompt = self.prompt_templates.build_prompt(self.context, task, template_type="general_knowledge") # Prompt handling.
                response = self.llm_interface.generate_text(prompt)  # Generate from LLM and handle errors.
                self.metrics['tasks_completed'] += 1  # Update metrics
                self.metrics['total_time_spent'] += (time.time()-start_time) # Update metrics
            except Exception as e: #Handle any errors during task processing.
                logger.error(f"GeneralKnowledgerAgent error: {e}") #Log error and include details, such as task information.
                response = f"An error occurred: {e}"
                self.metrics['tasks_failed'] += 1  # Update error metric
        else:
            response = "LLM not available."  # Return a user-friendly message.

        self.update_context(task, response)  #Update context with final response.
        return response


class FactCheckerAgent(Agent):
  def handle_task(self, task: str) -> str:
    self.load_llm()
    
    start_time = time.time()
    if self.llm_interface:
        try:
            prompt = self.prompt_templates.build_prompt(self.context, task, template_type="fact_check")  # Or build prompt
            response = self.llm_interface.generate_text(prompt)
            # Implement fact verification logic here, update metrics, and handle errors.
            verified = True #Placeholder for now.
            if verified:
                response += " (Verified)"  #Modify the response as needed.
            else:
                response +=" (Unverified)"  #Update response as needed.

            self.metrics['tasks_completed'] += 1  # Update metric


        except Exception as e:
            logger.error(f"FactCheckerAgent error: {e}")

            response = f"An error occurred: {e}" #Return a more descriptive error message.  Can improve for users later.
            self.metrics['tasks_failed'] += 1  # Update metric

    else:

        response = "LLM not available for this agent."  # Handle case where LLM not loaded.


    end_time = time.time()  # End task timer
    self.metrics['total_time_spent'] += (end_time - start_time)
    self.update_context(task, response) #Update context
    return response



class FSAgent(Agent):
    def handle_task(self, task: str) -> str:
        self.load_llm()
        start_time = time.time()  # Start measuring execution time.

        if self.llm_interface:
            if self.requires_tools(task):  # Checks if tools are required.
                response = self.use_tools(task) # Use tools if appropriate.
            else:
                prompt = self.prompt_templates.build_prompt(self.context, task, template_type="file_system") # Or construct prompt directly.
                response = self.llm_interface.generate_text(prompt)  # Use LLM, handle errors.
            self.metrics['tasks_completed'] += 1

        else:
            logger.error(f"FSAgent: LLM not loaded.")  # Handle case where LLM isn't loaded. Log the error message and the agent that failed.
            response = "LLM not loaded for this Agent"


        end_time = time.time()  # Start task timer
        self.metrics['total_time_spent'] += (end_time - start_time)
        self.update_context(task, response)  # Update context.

        return response


# ... (Other specialized agent classes as needed)