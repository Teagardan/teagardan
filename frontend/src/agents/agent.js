import React, { useState, useEffect, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { selectAgentById } from '../redux/agentSlice';
import { addTask, selectTasksByAgentId } from '../redux/taskSlice'; // Import task-related actions/selectors
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Typography, Button, List, ListItem, ListItemText, IconButton } from '@mui/material';
import TaskInput from './TaskInput';
import DeleteIcon from '@mui/icons-material/Delete';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';



const Agent = () => {
    const { agentId } = useParams();
    const dispatch = useDispatch();
    const navigate = useNavigate(); // For navigation
    const agent = useSelector((state) => selectAgentById(state, agentId));
    const agentTasks = useSelector(state => selectTasksByAgentId(state, parseInt(agentId, 10))); // Fetch tasks from the store
    const [newTask, setNewTask] = useState('');
    const [agentStatus, setAgentStatus] = useState('inactive'); // Initial status


    useEffect(() => {
        if (!agent) {
            navigate('/'); // Or to an error page
        }

    }, [agent, navigate]); //Add agent as dependency


    const handleStartAgent = async () => {
        try {
            // Make API call to start agent
            const response = await axios.post(`/agents/${agent.id}/start`); // Example API endpoint
            if (response.status === 200) {
                setAgentStatus('active');
            } else {
              throw new Error(`Could not start agent: ${response.status} ${response.statusText}`);
            }
            // Handle success (e.g., update agent status in Redux)

        } catch (error) {
            console.error('Error starting agent:', error);
            alert(error.message); // Display error message to the user.
        }
    };


    const handleStopAgent = async () => {
        try {
            // Make API call to stop agent
            const response = await axios.post(`/agents/${agent.id}/stop`); // Example API endpoint
            if (response.status === 200) {
                setAgentStatus('inactive'); // Update agent status and handle any other logic in your Redux store
            } else {
                throw new Error(`Could not stop agent: ${response.status} ${response.statusText}`);
            }


        } catch (error) {
            console.error('Error stopping agent:', error);
            alert(error.message); // Display error message to the user
        }
    };



    const handleTaskSubmit = async (taskDescription) => {
        if (agentStatus === "inactive") {
            alert("Agent is inactive, please start the agent first.");
            return;
        }

        try {
            const newTask = {
                id: uuidv4(),
                description: taskDescription,
                agentId: parseInt(agentId, 10), // Use agentId from route params
                status: 'pending' 
            };
            await dispatch(addTask(newTask)).unwrap(); // Dispatch action and await.  Error handling with unwrap().
            setNewTask(taskDescription);

        } catch (error) {
            console.error("Error submitting task:", error);
            alert(error.message);

        }

    };


  const handleDeleteTask = useCallback(async (taskId) => { // Use useCallback
    try {
      // Make API call to delete task
      await axios.delete(`/tasks/${taskId}`); // Example API endpoint
      // Update Redux store after successful deletion (you'll need to implement a deleteTask action in your taskSlice)


    } catch (error) {
        console.error("Error deleting task:", error);
        alert(error.message)

    }
}, []);


    if (!agent) {
        return (
            <Box sx={{ p: 2 }}>
                <Typography variant="h6">Agent not found.</Typography>

                <Button onClick={() => navigate('/')}>Back to Agent List</Button> {/*Add a "Back" button. */}
            </Box>

        );
    }



    return (
        <Box sx={{ p: 2 }}>


            <Typography variant="h5" component="h2" gutterBottom>Agent: {agent.name}</Typography>
            <Typography variant="body1" gutterBottom>Description: {agent.description}</Typography>
            <Typography variant="body1" gutterBottom>Skills: {agent.skills.join(', ')}</Typography>
            <Typography variant="body1" gutterBottom>Status: {agentStatus}</Typography> {/*Display Agent Status */}



            {/* Agent Controls */}
            <Box sx={{ mt: 2 }}>  {/*Buttons and handlers for starting/stopping agents. */}
                <Button variant="outlined" onClick={handleStartAgent} disabled={agentStatus === 'active'}>Start Agent</Button>
                <Button variant="outlined" color="secondary" onClick={handleStopAgent} disabled={agentStatus === 'inactive'} sx={{ ml: 2 }}>Stop Agent</Button>

            </Box>


            <TaskInput onSubmit={handleTaskSubmit} />


            {/* Task List  */}
            <Typography variant="h6" sx={{ mt: 3 }}>Agent Tasks:</Typography>
            <List>
                {agentTasks.map((task) => (  //Display agent tasks from Redux store.
                    <ListItem key={task.id} secondaryAction={  {/*Unique task ID as key */}
                        <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteTask(task.id)} > {/*Delete task button */}
                          <DeleteIcon />
                        </IconButton>
                      }>

                        <ListItemText primary={task.description} secondary={`Status: ${task.status}, Priority: ${task.priority}`} />
                    </ListItem>
                ))}

            </List>

        </Box>

    );
};


export default Agent;