import logging
import faiss  # For efficient similarity search (install with: pip install faiss-cpu)
import numpy as np
from sentence_transformers import SentenceTransformer #For sentence embeddings (install with: pip install sentence-transformers)
from typing import List, Dict, Any
#from sklearn.feature_extraction.text import TfidfVectorizer # For TF-IDF (if needed, install scikit-learn)
#from fuzzywuzzy import fuzz  # For Fuzzy Matching if not using other methods. (install with: pip install fuzzywuzzy)
import pickle  # For saving and loading embeddings


logger = logging.getLogger(__name__)



class MemoryManager:
    def __init__(self, embedding_model_name: str = 'all-mpnet-base-v2', embedding_dim: int = 768, memory_file: str = "memory.pkl"): #Uses default embedding model, can modify if needed.
        self.embedding_model_name = embedding_model_name
        try: #Initialize embedding model.
            self.embedding_model = SentenceTransformer(embedding_model_name) # Initialize here
        except Exception as e: #Handle potential errors while loading the model.
            logger.error(f"MemoryManager: Could not load SentenceTransformer model '{embedding_model_name}': {e}")
            self.embedding_model = None

        self.embedding_dim = embedding_dim
        self.memory: List[Dict[str, Any]] = []  # Stores messages and metadata
        self.index = None # Initialize FAISS index
        self.memory_file = memory_file  # File to save/load memory

        self.load_memory()  # Load saved memory if exists.



    def load_memory(self): # Load memory if exists, otherwise create index

        try:
            with open(self.memory_file, 'rb') as f:
                self.memory = pickle.load(f) #Load memory

            self.build_index() #After loading, build the index on it.
        except (FileNotFoundError, EOFError):  # Handle if file does not exist
            self.build_index()  # Initialize a new FAISS index
            logger.warning("Memory file not found or empty. Creating a new memory.")
        except Exception as e: #Handle other exceptions loading memory.
            logger.error(f"MemoryManager.load_memory: Error loading memory: {e}")  # Log error


    def save_memory(self): # Save memory to the pickle file.
        try:
            with open(self.memory_file, "wb") as f:  # Correct file mode
                pickle.dump(self.memory, f) #Saves the memory to the pickle file.

        except Exception as e:
            logger.error(f"MemoryManager.save_memory: Error saving memory: {e}")  #Log error


    def generate_embeddings(self, text: str) -> np.ndarray or None: # Correct return type hint
        """Generates embeddings for given text using pre-trained model."""
        try:
            if self.embedding_model: #Ensures model exists before using it.
                return self.embedding_model.encode(text) #Get embedding
            else: #Handles case where embedding model was not loaded correctly.
                logger.error("MemoryManager.generate_embeddings: Embedding model not available.")
                return None  # Return None to signal error
        except Exception as e:
            logger.error(f"MemoryManager.generate_embeddings: Error generating embedding for '{text}': {e}")
            return None  #Handles cases where generation failed.



    def build_index(self): # Use FAISS index for similarity search

        if self.memory and self.embedding_model:  #Only build index if the embedding model has loaded correctly and there is existing memory.
            embeddings = np.array([entry['embedding'] for entry in self.memory if entry.get('embedding') is not None], dtype=np.float32)  #Create array from existing data, ignores items with no embeddings.  Converts to float32 to make sure FAISS can use it.
            self.index = faiss.IndexFlatL2(self.embedding_dim)  # Create the FAISS index
            if embeddings.size > 0: #Only add embeddings if the array exists.
                self.index.add(embeddings)  # Add to the index
        else:
            self.index = faiss.IndexFlatL2(self.embedding_dim)  # Create a new index if there's no memory or embedding model yet
            logger.warning("MemoryManager.build_index: Building a new index, since memory or embedding model not initialized correctly.")



    def add_memory(self, text: str, metadata: Dict[str, Any] = None, timestamp: datetime = None): #Correct signature to use metadata for other information.
        """Add text and metadata to memory."""

        embedding = self.generate_embeddings(text) #Generate embedding
        if embedding is not None: #If the embedding was generated correctly, continue with adding it to memory.
            memory_entry = {
                'text': text,
                'embedding': embedding,
                'metadata': metadata or {}, #Add metadata, initializes empty dictionary if there's no metadata
                'timestamp': datetime.now() if timestamp is None else timestamp #Use current time if not provided
            }

            self.memory.append(memory_entry)  #Add the information.

            if self.index:  #If there is an index, add embedding to the index.
                self.index.add(np.array([embedding], dtype=np.float32))  # Correct usage of np.array and correct type for FAISS

            self.save_memory()


    def manage_context(self, current_context: str, new_message: str, context_window: int = 2048) -> str:  # Implements context window management
        """Manages the context window, appending new messages and removing old ones as needed."""

        updated_context = (current_context + "\n" + new_message).strip()  #Combine current context and new message

        # Implement logic for managing size (e.g., tokens) and update updated_context by removing old messages.  Tokenization of context and messages is required.
        # Example (simple truncation based on characters - replace with token-based logic):

        if len(updated_context) > context_window:
            updated_context = updated_context[-context_window:] #Keep last part if context is too large.

        return updated_context


    def search(self, query: str, top_k: int = 5, min_score=0.0) -> List[Dict[str, Any]]:  #Type hinting, returns list of dict with text, metadata, timestamp, and similarity score
        """Searches memory for similar entries."""


        query_embedding = self.generate_embeddings(query) #Generate embedding from the query string

        if query_embedding is not None and self.index is not None:  #Check to make sure index and query embedding have been created
            D, I = self.index.search(np.array([query_embedding], dtype=np.float32), top_k) #Search


            results = []
            for i in range(top_k):  # Retrieve data for the top_k closest matches
              index = I[0][i]  #Get index of ith result

              if index >= 0 and index < len(self.memory): #Check if it's a valid index
                  score = 1- D[0][i]/2 # Normalize score. Scale from 0 to 1 where 0 is least similar, 1 is most similar.
                  if score>= min_score:  #Use min_score for threshold.
                      memory_entry = self.memory[index].copy()  # Make copy to avoid changing the memory directly
                      memory_entry['similarity_score'] = score
                      results.append(memory_entry)  # Add the relevant information.
            return results

        else:  #If the index is not available (no memory yet, or issue with the embedding model).  Include more handling here if needed.
            logger.warning(f"MemoryManager.search: Cannot perform search. Index or embedding model not available.")
            return [] # Return empty list if search isn't possible.