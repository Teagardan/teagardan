import logging
from typing import List, Dict, Any

from neo4j import GraphDatabase  # For Neo4j (install with: pip install neo4j)
# from rdflib import Graph, URIRef, Literal, BNode  # For RDFlib (optional - install with: pip install rdflib)

logger = logging.getLogger(__name__)


class KnowledgeGraph:
    def __init__(self, uri: str = "bolt://localhost:7687", username: str = "neo4j", password: str = "your_password", graph_name="TeagardanKnowledgeGraph"): # Default values - replace with your actual credentials
        self.driver = None
        self.uri = uri
        self.username = username
        self.password = password
        self.graph_name = graph_name

        try: #Try connecting, otherwise raise exception.  This helps in alerting you to any misconfigurations in your database, before attempting to use it.
            self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password)) #Establish connection

            logger.info("KnowledgeGraph: Connected to Neo4j database.")
        except Exception as e:
            logger.error(f"KnowledgeGraph: Error connecting to Neo4j: {e}")  # Logs the error and gives more information, such as incorrect credentials, etc.  Can add handling here for specific types of exceptions, e.g. authentication-related or network-related exceptions.





    def close(self):
        if self.driver:  #Check to make sure the driver exists before attempting to use it.  This helps avoid errors and makes the program more robust.

            self.driver.close()
            logger.info("KnowledgeGraph: Connection to Neo4j closed.")


    def create_node(self, node_type: str, properties: Dict[str, Any]) -> int or None: #Updated for better typing, returns node ID.
        """Creates a node in the graph."""
        if not self.driver:
            logger.error("KnowledgeGraph.create_node: Not connected to the database.") #Return more details about what went wrong.
            return None


        try:
            with self.driver.session() as session: #Use a session.  More robust.
                result = session.write_transaction(self._create_and_return_id, node_type, properties)  # Correct method call.
                logger.info(f"KnowledgeGraph.create_node: Created node with type '{node_type}' and properties '{properties}'. Node ID: {result}")  #Log and show information about created node.

                return result #Return the ID.
        except Exception as e:  #Handle any exception during the creation of a node.

            logger.error(f"KnowledgeGraph.create_node: Error creating node of type '{node_type}': {e}") # Log and include node type details.
            return None  # Or raise the exception if you need the calling code to handle it.  Returning None can signal that an error has occurred.




    @staticmethod  #staticmethod since this is only used within the create_node method and doesn't modify or use the instance state.
    def _create_and_return_id(tx, node_type, properties):
        """Internal function to create a node and return its ID."""

        # Uses f-strings for query construction.  Makes the query easier to read.  You can modify the query as needed if the structure of your database is different, or use an index if one is created for your database.
        query = f'''
            CREATE (n:{node_type} $props)
            RETURN id(n) AS node_id
        '''


        result = tx.run(query, props=properties)  #Correctly runs query with parameters.
        record = result.single()  # Get the single record from database response.  If no data is returned (error or invalid return), this raises an exception to be handled.
        return record["node_id"]  #Returns ID from the record.




    def create_relationship(self, source_node_id: int, target_node_id: int, relationship_type: str, properties: Dict[str, Any] = None) -> bool:  #Return boolean for success/failure.

        """Creates a relationship between two nodes."""
        if not self.driver:  #Ensure the driver exists.
            logger.error("KnowledgeGraph.create_relationship: Not connected to the database.") #Log error and return.  Use informative messages so you know which method or section is having the issue, and provide context and details.

            return False  # Signal error



        try:

            with self.driver.session() as session:
                session.write_transaction(self._create_relationship, source_node_id, target_node_id, relationship_type, properties)
                logger.info(f"KnowledgeGraph.create_relationship: Created relationship '{relationship_type}' between nodes {source_node_id} and {target_node_id} with properties {properties}.") #Log successful relationship creation and provide relevant details.

            return True  # Signal success
        except Exception as e: #Handle any exceptions during relationship creation.  Provide details about the exception to improve debugging later.
            logger.error(f"KnowledgeGraph.create_relationship: Error creating relationship of type '{relationship_type}': {e}") #Log the error and include details to make it easier to understand the error and what caused it.  Can improve later with more specific exception handling to handle different cases, or check for different errors, as this will improve debugging when issues arise.
            return False #Signal failure.




    @staticmethod #staticmethod since the function doesn't use self.
    def _create_relationship(tx, source_node_id, target_node_id, relationship_type, properties):
        """Inner function for relationship creation."""


        query = f"""
            MATCH (a) WHERE id(a) = $source_id
            MATCH (b) WHERE id(b) = $target_id
            CREATE (a)-[r:{relationship_type} $props]->(b)
            RETURN r
        """ # Uses parameterized query.

        properties = properties or {} #Handles case where the properties parameter is None, or empty.  If not using properties, can remove.


        tx.run(query, source_id=source_node_id, target_id=target_node_id, props=properties) #Execute the cypher query using neo4j, including properties and node ID parameters.





    def get_node(self, node_id: int) -> Dict[str, Any] or None:  #Use Dict for the node representation. Return None if not found.

        """Retrieves a node and its properties."""


        if not self.driver:

            logger.error("KnowledgeGraph.get_node:  Not connected to the database.")
            return None


        try:  #Error handling when getting node.  Handles exceptions such as connection or authentication errors, or invalid query or parameters given.

            with self.driver.session() as session: #Use session. More robust.

                node = session.read_transaction(self._get_node, node_id)  #Correct call
                return node
        except Exception as e:
            logger.error(f"KnowledgeGraph.get_node:  Error retrieving node with id {node_id}: {e}")  # Log error and include the node id, as this will make it easier to find and reproduce the error.

            return None  #Handles exception.




    @staticmethod  #staticmethod as self is not used.
    def _get_node(tx, node_id):  #Gets the node from the database, including all properties.

        #F-string for formatting the query string with node ID parameter.
        query = f"""
            MATCH (n) WHERE id(n) = $node_id
            RETURN n
        """

        result = tx.run(query, node_id=node_id)  #Execute the query with node_id

        record = result.single()  #Get single result from database. Raises exception if node not found.

        if record:
            node = record['n']  #Get node from response
            return dict(node)  # Convert node to dictionary (better for JSON serialization if needed)
        else:
            return None  #Or raise exception.  This signals that no node was retrieved.




    def search_nodes(self, query: str, node_type=None, properties=None) -> List[Dict[str, Any]]: #Return a list of dictionaries
        """
        Searches for nodes matching the given query and optional filters.
        """


        if not self.driver:
            logger.error("KnowledgeGraph.search_nodes: Not connected to the database.") #Log the error and specify.

            return [] # Return empty list on error.



        try:
            with self.driver.session() as session:

                nodes = session.read_transaction(self._search_nodes, query, node_type, properties)  # Correct call
                return nodes
        except Exception as e:  # Handle exception and include details.
            logger.error(f"KnowledgeGraph.search_nodes: Error during node search: {e}") #Log and show error info.  Can improve for users.

            return [] #Return empty list to indicate search failed.




    @staticmethod  #staticmethod since self is not used.
    def _search_nodes(tx, query, node_type, properties):
        """Inner function for node search."""


        #Base query.
        where_clause = ""
        if node_type:
            where_clause += f"n:{node_type} "  #Add filter for type if provided.
        if properties: #Add filter for properties if given.

            for key, value in properties.items():

                #Add query for each property.  You should sanitize values to avoid injection attacks.  You'll need to implement this as required for your specific property types.
                where_clause += f"AND n.{key} = '{value}' " if where_clause else f"n.{key} = '{value}' " 
        query = f"MATCH (n) WHERE {where_clause} RETURN n" if where_clause else "MATCH (n) RETURN n"
        # Use query to search.

        result = tx.run(query)
        nodes = [dict(record['n']) for record in result]
        return nodes

#(Optional) RDFlib implementation (uncomment if needed):

# class RDFKnowledgeGraph:
#   def __init__(self):
#     self.graph = Graph()

#   # ... Implement RDFlib-specific methods for node/relationship/query handling ...