import logging
import os
import re
from typing import Dict, Any

import requests
from bs4 import BeautifulSoup

# Set up logging
logger = logging.getLogger(__name__)

class WebsiteRAGTool:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}  #Updated user agent

    def run(self, task: str, url: str = None) -> str: #Updated method signature. Now returns string.
        """
        Extracts information from a website based on the given task and (optional) URL.
        If no URL is provided, attempts to extract URL from the task description.

        Args:
            task: The task describing what information to extract.
            url: The URL of the website.

        Returns:
            Extracted information or an error message if extraction fails or URL is invalid.
        """
        if not url: #If no URL was given
            url = self.extract_url_from_task(task) #Extract the url from the task.
            if not url:
                return "No URL provided or found in the task."  #Provide more detail to the user.


        try:  # Try accessing the webpage at the URL.

            response = requests.get(url, headers=self.headers, timeout=10)  # Timeout after 10s
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx). More robust error handling.

            soup = BeautifulSoup(response.content, "html.parser") #Create soup object for parsing.
            extracted_info = self.extract_information(task, soup) #Extract and return info.
            return extracted_info  #Return extracted info.


        except requests.exceptions.RequestException as e:  #Handles any request errors.
            logger.error(f"WebsiteRAGTool.run: Error accessing or processing URL '{url}': {e}")  #Logs error, includes URL.
            return f"Could not access or process URL: {e}" #Return error message.  Can be more specific.


    def extract_url_from_task(self, task: str) -> str:
        """
        Extracts URL from the task description using regex.
        Can be improved with more robust NLP techniques.

        Args:
            task: The task description.

        Returns:
             The extracted URL or None if no URL is found.
        """
        try:
            # Regular expression to find URLs in the task description.
            url_pattern = re.compile(r"https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)")  #Handles variety of valid URL characters.


            match = url_pattern.search(task) #Searches for url using pattern
            if match:
                return match.group(0)  #Returns extracted url
            else:
                return None #If the URL is not found.

        except Exception as e:  #Handles exceptions when extracting URL.
            logger.error(f"extract_url_from_task:  Error extracting url: {e}")  #Log the error.


            return None




    def extract_information(self, task: str, soup: BeautifulSoup) -> str:  #Updated method signature.
        """
        Extracts relevant information from the parsed website content (soup).

        Args:
            task: Task describing information to extract (e.g., "Find the price").
            soup: Parsed BeautifulSoup object.

        Returns:
             Extracted information from the site or a message indicating failure.
        """

        # Placeholder implementation (replace with your actual extraction logic).

        # This is where you implement page-specific or query-specific extraction.
        # Example: Find and return the title, or text in first paragraph:
        try:
            if "title" in task.lower(): #Checks if the user wants the title
                title = soup.title.string  #Gets title
                if title: #If the title was retrieved, return it, otherwise, return that it was not found.  This prevents the application from crashing if the title is not found, and helps debug and improve page or query-specific handling later.
                  return title.strip()  #Return the extracted text and remove extra spaces around it.
                else:
                    return "Title not found on page." #Handles pages without titles.


            # Implement other extraction logics based on keywords in `task`
            # E.g., if "price" in task.lower(): extract price, etc.
            elif "first paragraph" in task.lower():
                first_p = soup.find('p')
                if first_p:
                    return first_p.get_text(strip=True)  # Correct way to extract and return stripped text from tag element
                else:  #Handles edge cases where there is no paragraph, for a more robust function.
                    return "No paragraphs found on page."


            return "No specific extraction criteria found in task."  #Return information about why extraction failed.
        except Exception as e:  #Catches any exception to prevent crashing, logs error and returns feedback.
            logger.error(f"extract_information: Error during information extraction: {e}")  # Logs the error. Include details like the task.

            return f"Error extracting information: {e}" #Fallback, more informative.