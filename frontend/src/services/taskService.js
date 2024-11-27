import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001'; // Or your backend base URL

const taskService = {
    fetchTasks: async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/tasks`);
            return response.data;
        } catch (error) {
            console.error("Error fetching tasks:", error);
            throw error; 
        }
    },

    addTask: async (newTask) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/tasks`, newTask);
            return response.data;
        } catch (error) {
            console.error("Error adding task:", error);
            throw error;
        }
    },

    updateTask: async (updatedTask) => {
        try {
            const response = await axios.put(`${API_BASE_URL}/tasks/${updatedTask.id}`, updatedTask); // PUT request for updates
            return response.data;
        } catch (error) {
            console.error("Error updating task:", error);
            throw error;
        }
    },

    deleteTask: async (taskId) => {
        try {
            const response = await axios.delete(`${API_BASE_URL}/tasks/${taskId}`);
            if (response.status !== 200 && response.status !== 204) { // Check for success status codes.
              throw new Error(`Failed to delete task: ${response.status} ${response.statusText}`); // More helpful error messages.
            }
          return true;
        } catch (error) {
            console.error("Error deleting task:", error);
            throw error;
        }
    },
    benchmarkTasks: async (tasks) => {  // Example: Benchmark a set of tasks
        try {
          const response = await axios.post(`${API_BASE_URL}/tasks/benchmark`, tasks);  //Update endpoint if needed.
          return response.data;
        } catch (error) {
            console.error("Error benchmarking tasks:", error);

            throw error;

        }
      },



    queueTask: async (task) => {
        try {
          const response = await axios.post(`${API_BASE_URL}/tasks/queue`, task); // Example endpoint for queuing.  Update if needed.
          return response.data;
        } catch (error) {
          console.error("Error queuing task:", error);
          throw error;
        }
      }
};


export default taskService;