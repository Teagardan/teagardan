import logging
import os
from typing import Dict, Any

from googleapiclient.discovery import build  # For Google Custom Search API
#from serpapi import GoogleSearch  # For SerpAPI (alternative)

# Set up logging
logger = logging.getLogger(__name__)

class WebSearchTool:
    def __init__(self, api_key: str, search_engine_id: str = None):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.service = None # Initialize the Google Custom Search service

        try:  # Initialize Google Custom Search API service
            self.service = build("customsearch", "v1", developerKey=self.api_key)
        except Exception as e:
            logger.error(f"WebSearchTool: Error initializing Google Custom Search: {e}")



    def run(self, query: str) -> str:  # Generic run method
        """
        Performs a web search using the provided query.

        Args:
            query: The search query string.

        Returns:
            A formatted string containing the search results, or an error message if the search fails.
        """
        try:
            if self.service:  # Check if the API service is initialized.  Use SerpAPI as fallback if not.

                results = self.google_custom_search(query)  # Use Google Custom Search API
            #elif self.serpapi_key:  # Use SerpAPI if available (and Google Custom Search is not)
               # results = self.serpapi_search(query)
            else: #Handle the case where the service is not available.
                return "No web search API configured."  # Error message

            return self.format_results(results)  #Format the returned results, handling errors appropriately.


        except Exception as e:
            logger.error(f"WebSearchTool.run: Error during web search: {e}") #Log the error and include details like the query.
            return f"Web search failed: {e}"



    def google_custom_search(self, query: str) -> Dict[str, Any]:  #Handles the API call and returns the raw data.
        """Makes the actual API call to Google Custom Search."""

        try:
            res = self.service.cse().list(q=query, cx=self.search_engine_id).execute() #Make the API request.

            return res  # Return raw response
        except Exception as e: #Handles errors that occur during the API call.
            logger.error(f"google_custom_search:  Error during search: {e}")  # Logs and includes details of what went wrong, such as the query string used.

            return None


    # def serpapi_search(self, query: str) -> Dict[str, Any]: #Uncomment if using SerpAPI as fallback.
    #    """Performs a web search using SerpAPI."""
    #    try:
    #         search = GoogleSearch({"q": query, "api_key": self.serpapi_key}) #Make the search request.
    #         results = search.get_dict() #Get the result as dictionary.
    #         return results  # Return raw response
    #     except Exception as e:
    #         logger.error(f"WebSearchTool.serpapi_search: Error during web search: {e}") #Logs the error and details, like query and key.
    #         return None


    def format_results(self, results: Dict[str, Any]) -> str:
        """Formats the search results into a user-friendly string."""

        if not results:
          return "No results found."

        formatted = ""
        try: #Try formatting data from Google Custom Search API
            for item in results.get("items", []): #Iterate through search result items.

                title = item.get("title")  #Extract title
                link = item.get("link") #Extract link
                snippet = item.get("snippet")  #Extract snippet


                formatted += f"Title: {title}\nURL: {link}\nDescription: {snippet}\n\n" #Format into a user-friendly string


        #except KeyError as e:  # Handles cases where keys aren't found (wrong API used?).  This gives more details about the missing keys, so that you know how to handle different response formats, which will help if you are integrating multiple APIs.  This also alerts you to potential issues with accessing values that may not exist in the data, so you can handle cases where keys or values are missing, which would prevent crashes from occurring when the actual data doesn't match the format or structure of what was expected, and improves debugging capability.
           # logger.error(f"format_results: KeyError: Missing key {e} in search results.")
           # return "Unexpected search result format.  Could not parse results." #Error handling.  Return an error message when format is incorrect.  Can improve message for users later.
        except Exception as e:
            logger.error(f"format_results: Error formatting results: {e}") #Logs the error.  Can improve for users later.
            return "Error formatting search results."

        return formatted  # Return the formatted results string.