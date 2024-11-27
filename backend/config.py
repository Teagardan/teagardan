# utils/config.py
import os
import json
from typing import Dict, Any  # Import Any
import logging

# Configure logging (optional but recommended)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)


def load_config(config_path: str = "config.json") -> Dict[str, Any]: # Type hint, and uses json by default
    """Loads configuration from a JSON file. Handles missing files or parsing errors."""
    try:
        with open(config_path, 'r') as f: #Opens file.  Can change 'r' to 'rb' if the file contains binary data.  Using 'r' makes it simpler if using text or JSON.

            config = json.load(f)
            return config

    except FileNotFoundError:

        logger.error(f"Config file '{config_path}' not found.")  #Logs the error and indicates which file is missing.  You can implement default values here if necessary.
        return {} #Returns empty config if file not found.
    except json.JSONDecodeError as e:  #Handles any invalid JSON values.
        logger.error(f"Error parsing config file: {e}") #Logs error and provides details about error.

        return {} # Return empty config on parsing error.  Or handle in another way (e.g., raise an exception)



#Get config using default config path.
CONFIG = load_config()

#Access config values like this:

#DATABASE_URI = CONFIG.get("database", {}).get("uri")  # Correct and safer access
#API_KEY = CONFIG.get("api_keys", {}).get("openai_api_key") #Example


#Or, you could structure the config like this for direct (but less safe) access:
#DATABASE_URI = CONFIG.get("DATABASE_URI")
#API_KEY = CONFIG.get("OPENAI_API_KEY")

# ... (other config variables) ...

#Example:  Ensure the models directory exists.  This function will attempt to create a directory if one does not exist.  If directory creation fails, it will log the error.

MODELS_DIR = CONFIG.get("MODELS_DIR", "./models") #Default value


try:  # Create models directory if it doesn't exist. This will handle the directory management for where to save and load models from.
    os.makedirs(MODELS_DIR, exist_ok=True) #Creates directory if needed.

except OSError as e:  # Handle potential errors in directory creation.

    logger.error(f"Could not create models directory: {e}")