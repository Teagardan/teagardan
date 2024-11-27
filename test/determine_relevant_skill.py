import unittest
from agent import Agent  # Import the Agent class

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

    def test_determine_relevant_skill_web_search(self):
        task = "Can you tell me the main features of the iPhone 14 Pro?"
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

if __name__ == '__main__':
    unittest.main()