import logging
import os
import shutil
from typing import List, Dict, Any

# Set up logging
logger = logging.getLogger(__name__)


class FileSystemTool:
    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir
        # Create the base directory if it doesn't exist.
        if not os.path.exists(self.base_dir):
          try: # Create base_dir recursively. This will ensure that operations can be performed in the specified directory without issues and that all necessary parent or child directories also exist to support a variety of file and directory operations.
            os.makedirs(self.base_dir)
          except OSError as e:
            logger.error(f"FileSystemTool: Could not create base directory '{self.base_dir}': {e}")  #Log the error and provide useful info.
        

    def run(self, task: str) -> str:
        """
        Executes file system operations based on the task description.

        Args:
            task: The task string (e.g., "read file.txt", "write 'hello' to new_file.txt", "list files", "create directory my_dir").

        Returns:
            The result of the file operation (file content, success/error message, list of files) or a message indicating an invalid task.
        """
        try:
            if "read" in task.lower():  # File reading.  Assumes filename after "read ".
                file_name = task.lower().split("read", 1)[1].strip()  # Extract filename.
                return self.read_file(file_name)

            elif "write" in task.lower():   # File writing
                # Assumes format "write content to file"
                match = re.search(r"write (.+) to (.+)", task.lower()) #Extracts the content and path using regex, using capture groups.  This will ensure that you can identify the parts of the string you are trying to extract without issue.

                if match: #If it matches this format
                    content = match.group(1).strip("'\"") #Extract the content to be written and strips quotes from it.
                    file_name = match.group(2).strip() #Extract the file name and removes extra whitespace.
                    return self.write_file(file_name, content)  #Write the content to the file.
                else:  #Handles invalid task strings and informs the user, which also assists in debugging by providing feedback.
                    return "Invalid 'write' task format.  Use: 'write content to filename'."

            elif "list files" in task.lower(): # File listing
                return self.list_files()

            elif "create directory" in task.lower():   #Directory creation
                dir_name = task.lower().split("create directory", 1)[1].strip()
                return self.create_directory(dir_name)

            elif "delete" in task.lower():   # File/directory deletion.
              # Extract filename or directory path after "delete"
                file_or_dir_name = task.split("delete", 1)[1].strip()
                return self.delete_file_or_directory(file_or_dir_name) #Handle deletion

            elif "copy" in task.lower():  #File copying.
                match = re.search(r"copy (.+) to (.+)", task.lower())  #Copy logic.
                if match:
                    source = match.group(1).strip()
                    destination = match.group(2).strip()
                    return self.copy(source, destination)
                else:
                    return "Invalid 'copy' task format. Use 'copy source to destination'"

            elif "move" in task.lower():  #File moving.
                match = re.search(r"move (.+) to (.+)", task.lower())  #Extract file name or directory after 'move'
                if match:
                    source = match.group(1)
                    dest = match.group(2)

                    return self.move(source, dest)  #Move the file, or folder.
                else:

                    return "Invalid 'move' task format. Use: 'move source to destination'" #Informative message and helps in debugging.
            
            return "Invalid file system task."  # Fallback error message.

        except Exception as e:  #Generic error handling with logging.  Handles errors gracefully.
            logger.error(f"FileSystemTool.run: Error executing task '{task}': {e}")  #Logs and includes task string.
            return f"File system task failed: {e}"  #Returns error message.




    def read_file(self, file_name: str) -> str:
        """Reads and returns the contents of file within base_dir.  Handles errors."""

        file_path = os.path.join(self.base_dir, file_name)  #Adds base directory to file path

        try:  #Error handling
            with open(file_path, 'r') as f:
                content = f.read() #Reads content of file.
            return content
        except FileNotFoundError:  #Specific handling if the file is not found.
            return f"File '{file_name}' not found." #Provides more feedback to the user.


        except Exception as e:  #General handling of exceptions.  Can modify as needed.
            logger.error(f"read_file: Error reading file '{file_name}': {e}")  #Logs error.  Includes file name.
            return f"Error reading file: {e}" #Returns error.  Can update for users later.






    def write_file(self, file_name: str, content: str) -> str:
        """
        Writes text content to a file within the base_dir.
        Creates the file if it doesn't exist. Handles errors and overwrites existing files.
        """
        file_path = os.path.join(self.base_dir, file_name)
        try:  #Handles any exceptions gracefully.
            with open(file_path, 'w') as f:  # Opens in write mode ('w').  Overwrites!
                f.write(content)  # Writes content to the file
            return f"Successfully wrote to '{file_name}'." #Success message.  Update for users later, if needed.

        except Exception as e: #Handles any exceptions during write.
            logger.error(f"write_file: Error writing to '{file_name}': {e}") #Logs the error.  Provides details.
            return f"Error writing to file: {e}"  #Handles errors.





    def list_files(self) -> str:  # Change return type to string for consistency.
        """
        Lists all files and directories in the base directory.
        Formats the list for better readability. Handles errors.
        """

        try:  #Error handling during file listing.
            files_and_dirs = os.listdir(self.base_dir)  # Get the list.

            # Formats into user-friendly string:
            if files_and_dirs:
                formatted_list = "\n".join(files_and_dirs) #Formats list of files, separated by \n.


                return f"Files and directories in '{self.base_dir}':\n{formatted_list}"
            else:
                return f"No files or directories found in '{self.base_dir}'." #Fallback.  Handles cases where the list is empty.  Provides feedback.


        except Exception as e:
            logger.error(f"list_files: Error listing files in '{self.base_dir}': {e}")  #Logs any errors.  Includes useful information, such as the base directory being used.

            return f"Could not list files: {e}" #Handles any errors that occurred during file listing.




    def create_directory(self, dir_name: str) -> str:
        """Creates a directory (and any missing parent directories) within the base_dir."""

        dir_path = os.path.join(self.base_dir, dir_name)  #Forms path.

        try: #Error handling and logging

            os.makedirs(dir_path, exist_ok=True)  # Use `exist_ok=True` to prevent error if directory already exists
            return f"Directory '{dir_name}' created successfully."
        except Exception as e:  #Exception handling for directory creation failure.
            logger.error(f"create_directory:  Error creating directory '{dir_name}': {e}") #Logs error and provides relevant details, such as the directory name.

            return f"Could not create directory '{dir_name}'. {e}"




    def delete_file_or_directory(self, name: str) -> str:
        """Deletes a file or directory (if empty)."""

        path = os.path.join(self.base_dir, name)  #Constructs path.
        try:
            if os.path.isfile(path):
                os.remove(path)  #Deletes file
                return f"File '{name}' deleted successfully."
            elif os.path.isdir(path):
                os.rmdir(path)  #Deletes empty directory
                return f"Directory '{name}' deleted successfully."
            else:
                return f"'{name}' is not a file or directory." #Fallback.
        except OSError as e: #Catches error when deleting.
            logger.error(f"delete_file_or_directory: Error deleting '{name}': {e}") #Logs error and provides detail.
            return f"Error deleting '{name}': {e}"  #Handles exception when deleting the folder.



    def copy(self, source, dest):
        src_path = os.path.join(self.base_dir, source)
        dest_path = os.path.join(self.base_dir, dest)
        try:  #Try copying recursively (handles directories).  Creates dest directory if necessary.
            if os.path.exists(src_path):
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, dest_path)  # `copy2` preserves metadata.
                elif os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                return f"Copied '{source}' to '{dest}'."
            else:
                return f"Source '{source}' not found."  #Error handling.  Alert user source is not valid.
        except Exception as e:
            logger.exception(f"copy: Error copying '{source}' to '{dest}': {e}")
            return f"Could not copy '{source}' to '{dest}': {e}"

    def move(self, src, dst):
        src_path = os.path.join(self.base_dir, src)
        dst_path = os.path.join(self.base_dir, dst)
        try:
          if os.path.exists(src_path):  #Checks if the path exists before moving.
              shutil.move(src_path, dst_path, dirs_exist_ok=True)  # `dirs_exist_ok=True` handles case where destination folder exists.  Use shutil.move, to correctly handle file or directory moving.
              return f"Moved '{src}' to '{dst}'"

          else:
              return f"Source '{src}' does not exist" #Provide better feedback to the user.  Improve debugging by indicating source is invalid.
        except Exception as e:
            logger.exception(f"move: Error moving: {e}")
            return f"Error moving '{src}' to '{dst}': {e}"