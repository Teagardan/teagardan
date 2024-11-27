import unittest
from agent import Agent  # Import the Agent class
from agent_system import AgentSystem  # Import AgentSystem
from llm_interface import LLM_Interface  # Import LLM_Interface
from memory_manager import MemoryManager  # Import MemoryManager

class TestAgent(unittest.TestCase):
    def setUp(self):
        # Create an instance of the Agent class for testing
        self.agent = Agent(name="Test Agent", description="For testing purposes", skills={
            "web search": "_ACTUAL_PATH_/llama.cpp/llama-3.2-3b-instruct-q8_0.gguf",
            "extract from website": "_ACTUAL_PATH_/llama.cpp/llama-3.2-3b-instruct-q8_0.gguf",
            "access files": "_ACTUAL_PATH_/llama.cpp/llama-3.2-3b-instruct-q8_0.gguf",
            "extract from document": "_ACTUAL_PATH_/llama.cpp/llama-3.2-3b-instruct-q8_0.gguf",
            "access website experts": "_ACTUAL_PATH_/llama.cpp/llama-3.2-3b-instruct-q8_0.gguf",
            "philosophical reasoning": "_ACTUAL_PATH_/llama.cpp/llama-3.2-3b-instruct-q8_0.gguf"
        })

        # Create an AgentSystem instance for testing
        self.llm_interface = LLM_Interface(model_path="_ACTUAL_PATH_/llama.cpp/llama-3.2-3b-instruct-q8_0.gguf") 
        self.llm_interface.load_model()  # Load the model explicitly
        self.agent_system = AgentSystem(self.llm_interface, MemoryManager()) 

    def test_determine_relevant_skill_web_search(self):
        task = "Can you search for the main features of the iPhone 14 Pro?"
        skill = self.agent.determine_relevant_skill(task)
        self.assertEqual(skill, "web search")

    def test_determine_relevant_skill_extract_from_website(self):
        task = "Extract information from the website about iPhone 14 Pro features"
        skill = self.agent.determine_relevant_skill(task)
        self.assertEqual(skill, "extract from website")

    def test_determine_relevant_skill_access_files(self):
        task = "Read the content of data.txt file"
        skill = self.agent.determine_relevant_skill(task)
        self.assertEqual(skill, "access files")

    def test_determine_relevant_skill_extract_from_document(self):
        task = "Extract information from the document about iPhone 14 Pro features"
        skill = self.agent.determine_relevant_skill(task)
        self.assertEqual(skill, "extract from document")

    def test_determine_relevant_skill_access_website_experts(self):
        task = "Find an expert on iPhone 14 Pro features"
        skill = self.agent.determine_relevant_skill(task)
        self.assertEqual(skill, "access website experts")

    def test_determine_relevant_skill_philosophical_reasoning(self):
        task = "What is the meaning of life?"
        skill = self.agent.determine_relevant_skill(task)
        self.assertEqual(skill, "philosophical reasoning")

    def test_determine_relevant_skill_no_match(self):
        task = "Do you like pizza?"
        skill = self.agent.determine_relevant_skill(task)
        self.assertIsNone(skill)
        
    def test_decompose_task(self):
        task = "Write a blog post about the benefits of using a knowledge graph in AI."
        decomposed_tasks = self.agent_system.decompose_task(task)
        self.assertTrue(any("research" in subtask.lower() for subtask in decomposed_tasks))  # Check for research concept
        self.assertTrue(any("benefit" in subtask.lower() for subtask in decomposed_tasks))  # Check for benefits concept
        self.assertTrue(any("knowledge graph" in subtask.lower() for subtask in decomposed_tasks))  # Check for knowledge graph concept
        self.assertTrue(any("outline" in subtask.lower() for subtask in decomposed_tasks))  # Check for outline concept
        self.assertTrue(any("write" in subtask.lower() for subtask in decomposed_tasks))  # Check for writing concept

if __name__ == '__main__':
    unittest.main()