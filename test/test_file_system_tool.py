import unittest
from file_system_tool import FileSystemTool
import os
import tempfile

class TestFileSystemTool(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()  # Create temporary directory for testing
        self.tool = FileSystemTool(self.temp_dir)  # Create FileSystemTool instance for testing

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)  # Clean up temporary directory after tests

    def test_read_file(self):
        file_path = os.path.join(self.temp_dir, "test.txt")
        with open(file_path, "w") as f:
            f.write("Hello, world!")
        self.assertEqual(self.tool.read_file("test.txt"), "Hello, world!")

    def test_read_nonexistent_file(self):
        self.assertEqual(self.tool.read_file("nonexistent.txt"), f"Error: File 'nonexistent.txt' not found in '{self.temp_dir}'.")

    def test_write_file(self):
        file_path = os.path.join(self.temp_dir, "output.txt")
        result = self.tool.write_file("output.txt", "This is test content.")
        self.assertEqual(result, f"File 'output.txt' written successfully to '{self.temp_dir}'.")
        self.assertTrue(os.path.exists(file_path))  #Check if the file exists.
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), "This is test content.")

    def test_write_file_in_subdir(self):
        file_path = os.path.join(self.temp_dir, "subdir", "output2.txt")
        result = self.tool.write_file("subdir/output2.txt", "Content in subdirectory")
        self.assertEqual(result, f"File 'subdir/output2.txt' written successfully to '{self.temp_dir}'.")
        self.assertTrue(os.path.exists(file_path))
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), "Content in subdirectory")

    def test_error_handling(self):
      #Simulate an error by attempting to write to a read-only file.
      #For example, on MacOS you might try this:
        #file_path = os.path.join(self.temp_dir, "readonly.txt")
        #os.chmod(file_path, 0o444)  # Set read-only permissions
        #result = self.tool.write_file("readonly.txt", "This should fail")
        #self.assertIn("Error writing", result)

        file_path = os.path.join(self.temp_dir, "readonly.txt")
        with open(file_path, 'w') as f:
            f.write("Hello")
        os.chmod(file_path, 0o444)
        result = self.tool.write_file("readonly.txt", "This should fail")
        self.assertIn("Error writing", result)

if __name__ == "__main__":
    unittest.main()