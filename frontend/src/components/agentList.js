import React, { useState, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { addAgent, terminateAgent, selectAgent as selectReduxAgent } from '../redux/agentSlice';
import AgentForm from './AgentForm';
import { List, ListItem, ListItemText, Button, Typography } from '@mui/material'; // Or your UI components



const AgentList = () => {
    const dispatch = useDispatch();
    const agents = useSelector(state => state.agents.agents);
    const selectedAgentId = useSelector(state => state.agents.selectedAgentId);
    const [showAgentForm, setShowAgentForm] = useState(false);



    const handleAgentSelect = (agent) => {
        dispatch(selectReduxAgent(agent.id));
    };




    const handleTerminateAgent = useCallback(async (agentId) => {
        try {
            await dispatch(terminateAgent(agentId)).unwrap();
        } catch (err) {
            console.error("Failed to terminate agent:", err);
            alert(`Failed to terminate agent ${agentId}. See console for details.`);
        }
    }, [dispatch]);


    const handleAddAgent = async (newAgent) => {
        try {
            await dispatch(addAgent(newAgent)).unwrap();
            setShowAgentForm(false);
        } catch (error) {
            console.error("Error adding agent:", error);
            alert(error.response ? error.response.data.error : error.message); // Alert with error message
        }
    };




    const handleOpenAgentForm = () => {
        setShowAgentForm(true);
    };



    const handleCloseAgentForm = () => {
        setShowAgentForm(false);
    };



    return (
        <div>
            <Typography variant="h5" component="h2">  {/* Example heading */}
                Agent List  
            </Typography>

            <List> {/* Use a List component for better structure */}
                {agents.map((agent) => (
                    <ListItem 
                        key={agent.id} 
                        button
                        selected={agent.id === selectedAgentId} 
                        onClick={() => handleAgentSelect(agent)}
                        secondaryAction={(  // For better button placement
                            <Button variant="outlined" color="secondary" size="small" onClick={(e) => {
                                e.stopPropagation(); 
                                handleTerminateAgent(agent.id);
                            }}>
                                Terminate
                            </Button>
                        )}
                    >
                        <ListItemText primary={`${agent.name} (${agent.type || 'N/A'})`} secondary={`Skills: ${agent.skills.join(', ')}`} />


                    </ListItem>
                ))}
            </List>


            <Button variant="outlined" onClick={handleOpenAgentForm}>
                Add Agent
            </Button>


            {/* Show the form conditionally */}
            {showAgentForm && (
                <AgentForm open={showAgentForm} onClose={handleCloseAgentForm} onSubmit={handleAddAgent} />
            )}
        </div>
    );
};



export default AgentList;