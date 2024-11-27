import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Routes, Route, useNavigate, useParams } from 'react-router-dom';
import { loadAgents } from '../redux/agentSlice';
import { loadMessages } from '../redux/messageSlice';
import AgentList from './AgentList';
import Thread from './Thread';
import TaskInput from './TaskInput';
import AgentDetails from './AgentDetails';
import KnowledgeGraphVisualization from './KnowledgeGraphVisualization';
import TaskManagerUI from './TaskManagerUI';
import AgentConfigurationUI from './AgentConfigurationUI';
import SystemAdministrationUI from './SystemAdministrationUI';
import UserProfile from './components/UserProfile'; // Correct import paths
import Login from './components/Login';        // Correct import paths
import UserManagementUI from './components/UserManagementUI'; // Correct import paths
import { Box, Grid, Typography } from '@mui/material'; // Import necessary components
import { createTheme, ThemeProvider } from '@mui/material/styles'; //For theming, replace or modify if necessary.

const theme = createTheme();

const TeagardanUI = () => {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const { id } = useParams(); // For agent-specific routes
    const [error, setError] = useState(null);
    const selectedAgentId = useSelector(state => state.agents.selectedAgentId); // Access from store
    const [user, setUser] = useState(null);

    useEffect(() => {
        const loadAppData = async () => { // Combined data loading function.
          try {
            await dispatch(loadAgents()).unwrap();
            if (selectedAgentId) { // Load messages if an agent is selected
                await dispatch(loadMessages(selectedAgentId)).unwrap();
            }
          } catch (err) {
            console.error("Error loading data:", err);
            setError("Failed to load data.  See the console for details.");
          }
        };
        loadAppData();
      }, [dispatch, selectedAgentId]);


      //Handlers for login/logout, same as before:
    const handleLogin = (userData) => {
        setUser(userData);
        navigate('/profile');  //Or home page.
    };


    const handleLogout = () => {
        setUser(null);
        navigate('/login'); //Redirect after logout
    };




    return (
        <ThemeProvider theme={theme}> {/* If using a theme provider. */}
            <Box sx={{ flexGrow: 1, padding: theme.spacing(3) }}> {/* Grid container, and spacing.  If not using MUI, remove the padding sx attribute. */}

                <Grid container spacing={2}>
                    <Grid item xs={12}> {/*Page title.  Can modify as needed.  Can remove if not using MUI. */}
                        <Typography variant="h4">Teagardan</Typography>
                    </Grid>
                    <Grid item xs={3}> {/*Sidebar for agents and navigation. */}
                        <AgentList />
                    </Grid>


                    <Grid item xs={9}>  {/*Main content area (thread, details, etc.). */}
                        <Routes>
                            <Route path="/" element={selectedAgentId ? <navigate to = "/thread"/> : <p>Select an agent to start a conversation.</p>} />
                            <Route path="/thread" element={selectedAgentId ? (
                                <>
                                <Thread agentId={selectedAgentId} /> {/* Pass agentId */}

                                <TaskInput agentId={selectedAgentId}/>   {/* Pass agentId */}
                                </>
                            ) : (
                                <p>Select an agent to start a conversation.</p> 
                            )} />
                            <Route path="/agent/:id" element={<AgentDetails />} />                            
                            <Route path="/knowledge-graph" element={<KnowledgeGraphVisualization />} />
                            <Route path="/tasks" element={<TaskManagerUI />} />
                            <Route path="/agent-config" element={<AgentConfigurationUI />} />
                            <Route path="/admin" element={<SystemAdministrationUI />} />

                            <Route path="/login" element={<Login onLogin={handleLogin} />} />
                            <Route path="/profile" element={user ? <UserProfile user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
                            <Route path="/users" element={user ? <UserManagementUI /> : <Navigate to="/login" />} />

                            {/* ... other routes ... */}
                            <Route path="*" element={<p>There's nothing here: 404!</p>} /> 

                        </Routes>
                    </Grid>

                </Grid>
            </Box>
        </ThemeProvider>
    );

};

export default TeagardanUI;