import logging
from typing import List, Union  # Import Union for type hinting
import numpy as np
from sentence_transformers import SentenceTransformer  # For sentence embeddings
#from sklearn.feature_extraction.text import TfidfVectorizer # For TF-IDF (optional)


logger = logging.getLogger(__name__)



class Embeddings:
    def __init__(self, model_name: str = 'all-mpnet-base-v2', model: SentenceTransformer = None): #Default model, you can customize.
        self.model_name = model_name
        self.model = model or self.load_model(model_name) #Load on init.




    def load_model(self, model_name: str) -> SentenceTransformer:  # Correct return type hint. Load model and handles potential errors during model loading.
        """Loads the specified embedding model."""
        try:
            model = SentenceTransformer(model_name)
            return model

        except Exception as e: #Handles exceptions during model loading and provides a message.  This is better for logging and debugging.

            logger.error(f"Embeddings.load_model: Could not load model '{model_name}': {e}")
            return None



    def generate(self, text: Union[str, List[str]]) -> np.ndarray or None: # Type hint, handles list of strings, returns appropriate data structure.
        """Generates embeddings for the given text.  Handles single string or list of strings."""

        if not self.model:
            logger.error("Embeddings.generate: Embedding model not loaded.") #Error logging, provides context.
            return None


        try:  # Error handling during embedding generation.
            if isinstance(text, str):
                embeddings = self.model.encode(text) #Generate embeddings from the text

            elif isinstance(text, list):
                embeddings = self.model.encode(text) #Generate embeddings from the list.

            else: # If it is an invalid type.
                logger.error(f"Embeddings.generate: Invalid input type: {type(text)}. Expected string or list of strings.")
                return None

            return embeddings #Return embeddings
        except Exception as e:
            logger.error(f"Embeddings.generate: Error generating embeddings for '{text}': {e}") #Log error and details.
            return None  #If there is an error during generation, signal with None.




    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float or None:  # Type hinting, error handling
        """Calculates cosine similarity between two embeddings."""

        if not isinstance(embedding1, np.ndarray) or not isinstance(embedding2, np.ndarray): #Checks if the type is valid.
            logger.error(f"Embeddings.similarity: Invalid input type. Expected numpy arrays, but got {type(embedding1)} and {type(embedding2)}.")  # Log error, include type information.
            return None

        try:
          similarity_score = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)) #Cosine similarity calculation.

          return similarity_score #Return score.

        except Exception as e: #Handle errors during similarity calculation, for a more robust program and debugging.
            logger.error(f"Embeddings.similarity: Error calculating similarity: {e}")  # Log error, include more details, such as embedding values, types, shapes, or sizes.
            return None  # Or raise a more specific error if needed



    # Optional: TF-IDF Embeddings (uncomment if needed)
    # def generate_tfidf(self, texts: List[str]):
    #     vectorizer = TfidfVectorizer()  # Initialize the vectorizer
    #     tfidf_matrix = vectorizer.fit_transform(texts) # Fit and transform the text list.
    #     # ... (Rest of the implementation - get feature names, create dictionary, etc.)