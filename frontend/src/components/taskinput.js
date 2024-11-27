import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux'; // Import Redux hooks
import { addTask } from '../redux/taskSlice'; // Import your Redux action
import { TextField, Button, Box } from '@mui/material'; // Import UI components

const TaskInput = () => {
    const dispatch = useDispatch();
    const [taskDescription, setTaskDescription] = useState('');
    const selectedAgentId = useSelector(state => state.agents.selectedAgentId); // Get selectedAgentId from Redux


    const handleSubmit = async (e) => {
        e.preventDefault();


        if (!selectedAgentId) { // Check if an agent is selected
            alert('Please select an agent before submitting a task.');
            return;
        }

        try {
            // Create a new task object
            const newTask = {
                description: taskDescription,
                agentId: selectedAgentId, // Assign to selected agent
                status: 'pending' // Or 'new', depending on your workflow
            };

            await dispatch(addTask(newTask)).unwrap(); // Dispatch addTask action and await result for better error handling.  Handle potential rejections using unwrap().
            setTaskDescription(''); // Clear the input field
            // Optionally display a success message or update task list.


        } catch (error) {
            console.error("Error adding task:", error);
            // Handle the error appropriately (e.g., display an error message)
            alert(error.response ? error.response.data.error : error.message);
        }
    };


    return (
        <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}> {/* Wrap in a Box */}
            <TextField
                margin="normal"
                required
                fullWidth
                id="taskDescription"
                label="Task Description"
                name="taskDescription"
                autoFocus
                value={taskDescription}
                onChange={(e) => setTaskDescription(e.target.value)}
            />
            <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
            >
                Submit Task
            </Button>
        </Box>

    );
};


export default TaskInput;