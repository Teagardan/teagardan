import logging
from typing import Dict, Type, Any  # Import Any for type hinting
from tools.web_search_tool import WebSearchTool  # Example: Import your tools
from tools.website_rag_tool import WebsiteRAGTool
# ... import other tools

logger = logging.getLogger(__name__)


class ToolManager:
    def __init__(self):
        self.tools: Dict[str, Type[Any]] = {}  # Initialize tools dictionary with type hints.  Any allows for flexibility in tools.


    def register_tool(self, name: str, tool_class: Type[Any]): #Type hint
        """Registers a tool with the manager."""

        if name in self.tools:  #If name exists, give a warning.

            logger.warning(f"ToolManager: Tool with name '{name}' already registered.  Overwriting.")
        self.tools[name] = tool_class #Adds tool to list


    def unregister_tool(self, name: str):
        """Unregisters a tool."""

        if name not in self.tools:
            logger.warning(f"ToolManager: Tool with name '{name}' not registered.")
            return  # Or raise an exception if you prefer a stricter approach.  If not registered, then skip it.

        del self.tools[name]  # Remove tool from dictionary if it exists.


    def get_tool(self, name: str) -> Type[Any] or None: #Type hint the return to handle cases where the tool isn't found, and update how the name is retrieved.
        """Retrieves a registered tool class by name."""

        return self.tools.get(name) #Returns None if tool not found.  Handles KeyErrors.


    def initialize_tools(self, agent, api_key=None, search_engine_id=None):
        """
        Initializes and returns a list of tool instances based on agent's requested tools.
        Handles missing API keys or IDs gracefully.
        """

        initialized_tools = []
        for tool_name in agent.tools: #Iterates over agent's requested tools.
            if tool_name.lower() == "web_search":  # Check tool name
                if api_key and search_engine_id:  #Check if keys exist
                    try: #Try instantiating and adding tool, otherwise, raise exception and log error.  This handles cases where the tool is found, but the parameters are invalid.

                      tool = WebSearchTool(api_key, search_engine_id)
                      initialized_tools.append(tool)
                    except Exception as e:
                        logger.error(f"Tool '{tool_name}' initialization failed: {e}")  # Log initialization error with specific details about the tool and exception message
                else:
                    logger.warning(f"Tool '{tool_name}' requires an API key and search engine ID.") # More detailed logging, easier to debug.

            elif tool_name.lower() in self.tools:  #Use the correct tool name and handle cases where tools don't require keys.  This makes adding tools easier, since now, only tools that require an API key or other setup have to have error handling explicitly added.
                try:  # Try to initialize the tool with correct parameters or handle missing parameters.

                    tool_class = self.tools.get(tool_name.lower())
                    initialized_tools.append(tool_class())

                except Exception as e:  # Handle exceptions if additional parameters are missing or invalid.  This covers both instantiation and usage of the tool, handling errors.  This also gives more context, helping identify issues with specific tools more easily, and improves the debugging process.
                    logger.error(f"Tool '{tool_name}' initialization failed: {e}") #Logs and provides the tool and error information.
            else:  # Tool not recognized

                logger.warning(f"Tool '{tool_name}' not recognized.") # More helpful warning message.



        return initialized_tools


    def list_tools(self): # New method to get all available tools.
        """Returns a list of the names of all registered tools."""
        return list(self.tools.keys())  #Return names only.