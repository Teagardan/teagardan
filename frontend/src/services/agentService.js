import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001'; // Or your backend base URL

const agentService = {
    loadAgents: async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/agents`);
            return response.data;
        } catch (error) {
            console.error("Error loading agents:", error);
            throw error; // Re-throw the error to be handled by the component
        }
    },


    addAgent: async (newAgent) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/agents`, newAgent);
            return response.data;
        } catch (error) {
            console.error("Error adding agent:", error);
            throw error;
        }
    },



    updateAgent: async (updatedAgent) => {
        try {
          const response = await axios.put(`${API_BASE_URL}/agents/${updatedAgent.id}`, updatedAgent);  //Uses PUT for updates
          return response.data;

        } catch (error) {
            console.error("Error updating agent:", error);
            throw error;  //Re-throw
        }
    },


    terminateAgent: async (agentId) => {
        try {
          const response = await axios.delete(`${API_BASE_URL}/agents/${agentId}`);

            if (response.status !== 200) {
              throw new Error(`Failed to terminate agent: ${response.status} ${response.statusText}`); // More detailed error messages
            }
            return true;  
        } catch (error) {

            console.error('Error terminating agent:', error);
            throw error; //Re-throw the error to be handled by component

        }
    },


    reorderAgents: async (reorderedAgents) => {
        try{
            const response = await axios.post(`${API_BASE_URL}/agents/reorder`, reorderedAgents);  //POST request to reorder endpoint
            return response.data;
        } catch (error) {
            console.error("Error reordering agents:", error);
            throw error;
        }
    },




    fetchAgentTasks: async (agentId) => { // Fetches tasks for a given agent
        try {
            const response = await axios.get(`${API_BASE_URL}/agents/${agentId}/tasks`); // Example API endpoint
            return response.data; //Returns array of tasks
        } catch (error) {
            console.error("Error fetching agent's tasks:", error);
            throw error;
        }
    },




    startAgent: async (agentId) => {
        try{
            const response = await axios.post(`${API_BASE_URL}/agents/${agentId}/start`);  // Example API endpoint
            return response.data;
        } catch (error){
            console.error("Error starting agent:", error);
            throw error;
        }
    },



    stopAgent: async (agentId) => {
        try{
            const response = await axios.post(`${API_BASE_URL}/agents/${agentId}/stop`); // Example API endpoint.
            return response.data;
        } catch (error) {
            console.error("Error stopping agent:", error);
            throw error;
        }

    }
};



export default agentService;