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

class FactCheckerAgent(Agent):  # Inherits from the abstract Agent class
    def handle_task(self, task: str) -> str:
        self.load_llm()
        start_time = time.time()


        if self.llm_interface:  # Check if LLM loaded correctly
            try:
                prompt = self.prompt_templates.build_prompt(self.context, task, template_type="fact_check")  # Construct fact-checking prompt using the PromptTemplates class. You'll need to define the "fact_check" template in your PromptTemplates.
                response = self.llm_interface.generate_text(prompt)  #Send the prompt to the LLM and handle exceptions during response generation.

                # Extract the claim to be verified
                claim = self.extract_claim_from_task(task)

                if claim: #If it exists
                    verification_result = self.verify_claim(claim) #Verify the claim.

                    if verification_result.get("verified"): #Update with verification result
                      response += f" (Verified: {verification_result.get('evidence', 'No evidence provided.')})"
                    else:

                        response += f" (Unverified: {verification_result.get('evidence', 'No evidence provided.')})"


                self.metrics['tasks_completed'] += 1 #Update metrics, and add time elapsed since starting task.
                self.metrics['total_time_spent'] += (time.time() - start_time)

            except Exception as e:
                logger.error(f"FactCheckerAgent error: {e}")  # Log error
                response = f"An error occurred during fact-checking: {e}"
                self.metrics['tasks_failed'] += 1  # Update metrics for failure

        else:  #If the LLM is not loaded properly
            response = "LLM not available for this agent."


        self.update_context(task, response)  # Context update
        return response



    def extract_claim_from_task(self, task: str) -> str:
        """Extracts the claim to be fact-checked from the task description using simple string manipulation or regex.  Can be improved with more sophisticated NLP methods."""

        try:  # Example extraction using simple splitting (replace with your logic)
            # This example assumes the task format is like:
            # "Fact-check: <claim>" or "Check this: <claim>"

            if ":" in task:  # Extract substring after colon
              claim = task.split(":", 1)[1].strip() #Gets claim part of task

            elif "Fact-check" in task: # Handles "Fact-check <claim>"
                claim = task.split("Fact-check", 1)[1].strip()  # Extract claim

            elif "Check this" in task: #Handles "Check this: <claim>"
                claim = task.split("Check this", 1)[1].strip() #Get claim part of task
            else:  #If there is no colon or key phrase, then the entire message is considered the claim to be verified.
                claim = task.strip()  # The entire task description is the claim
            return claim
        except Exception as e:  #Catch any exception and log and handle.
            logger.error(f"extract_claim_from_task: Error extracting claim: {e}")

            return None #If extraction fails, then return None


    def verify_claim(self, claim: str) -> Dict[str, Any]:
        """
        Verifies a claim using available tools, external APIs, or knowledge bases.

        Returns:
            A dictionary containing:
            - 'verified': True if claim is verified, False otherwise.
            - 'evidence': Evidence supporting the verification result.
        """
        # Placeholder implementation (replace with actual verification logic).
        try:
            # This is where you would implement your fact-checking logic using:
            # - Tools in self.tools (e.g., WebSearchTool)
            # - External APIs (e.g., fact-checking APIs)
            # - Knowledge base lookups (if you have one)


            #For demonstration, this simple version searches for the claim in the memory manager and the web:
            memory_result = self.memory_manager.search(claim)
            web_search_results = self.use_tools(claim) if self.requires_tools(claim) else ""
            evidence = ""
            if memory_result:
                evidence += f"Memory: {memory_result}\n"
            if web_search_results:
                evidence += f"Web Search: {web_search_results}"

            verified = bool(memory_result or web_search_results)  #Placeholder logic
            return {"verified": verified, "evidence": evidence} # Return a dictionary containing whether the information was verified, and any relevant supporting evidence found.


        except Exception as e:  #Handles any errors during verification
            logger.error(f"FactCheckerAgent.verify_claim: Error verifying claim '{claim}': {e}") #Logs the error and provides details, such as the claim that failed to be verified.
            return {"verified": False, "evidence": f"Error during verification: {e}"}  #Fallback on error, provides feedback


#In main.py or wherever you create your agents:
#fact_checker = FactCheckerAgent(4, "Fact Checker", "Checks facts", ["fact-checking"], tools=["web_search"], api_key="YOUR_API_KEY", search_engine_id="YOUR_SEARCH_ENGINE_ID", model_path="path/to/model")