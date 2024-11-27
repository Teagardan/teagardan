import React, { useState, useEffect, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchAgents,
  updateAgent,
  selectAgentById,
  reorderAgents,
  terminateAgent
} from '../redux/agentSlice';
import {
  Box,
  List,
  ListItem,
  ListItemText,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
  IconButton,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Switch,
  FormControlLabel,
  FormGroup,
  Checkbox,
  ListItemSecondaryAction,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';



const AgentConfigurationUI = () => {
    const dispatch = useDispatch();
    const agents = useSelector((state) => state.agents.agents);
    const [editedAgent, setEditedAgent] = useState(null);
    const [editOpen, setEditOpen] = useState(false);
    const [isDragging, setIsDragging] = useState(false);


    useEffect(() => {
        dispatch(fetchAgents());
    }, [dispatch]);


    const handleOpenEditDialog = (agent) => {
        setEditedAgent({ ...agent });
        setEditOpen(true);
    };



    const handleCloseEditDialog = () => {
        setEditedAgent(null);
        setEditOpen(false);
    };



    const handleEditSubmit = async () => {
        try {
            await dispatch(updateAgent(editedAgent)).unwrap();
            handleCloseEditDialog();
        } catch (error) {
            console.error("Error updating agent:", error);
            alert(error.response ? error.response.data.error : error.message);
        }
    };




    const handleInputChange = (e) => {
        setEditedAgent({ ...editedAgent, [e.target.name]: e.target.value });
    };


    const handleSkillChange = (e, index) => {
        const newSkills = [...editedAgent.skills];
        newSkills[index] = e.target.value;
        setEditedAgent({ ...editedAgent, skills: newSkills });

    };


    const handleAddSkill = () => {
        setEditedAgent({ ...editedAgent, skills: [...editedAgent.skills, ''] });

    };



    const handleToolChange = (event) => {
        const { options } = event.target;
        const value = [];
        for (let i = 0, l = options.length; i < l; i += 1) {
          if (options[i].selected) {
            value.push(options[i].value);
          }
        }
        setEditedAgent({ ...editedAgent, tools: value });
      };



    const handleRoleChange = (event) => {
        setEditedAgent({ ...editedAgent, role: event.target.value });

    };


    const handlePermissionChange = (event) => {
        const { name, checked } = event.target;
        setEditedAgent({ ...editedAgent, permissions: { ...editedAgent.permissions, [name]: checked } });

    };




    const handleAgentStatusChange = (agentId, newStatus) => {
        dispatch(updateAgent({ id: agentId, status: newStatus }));
    };

    const handleTerminateAgent = useCallback(async (agentId) => { // Ensure useCallback is used correctly
        try {
            await dispatch(terminateAgent(agentId)).unwrap();
            // Optionally, you can refetch agents or remove the terminated agent from state here
        } catch (error) {
            console.error("Failed to terminate agent:", error);
            alert(`Failed to terminate agent ${agentId}. See console for details.`);
        }
    }, [dispatch]);  // Include dependencies


    const handleOnDragEnd = (result) => {
        setIsDragging(false);


        if (!result.destination) {
          return;
        }
      
        dispatch(reorderAgents({
          sourceIndex: result.source.index,
          destinationIndex: result.destination.index
        }));
    };




    const handleOnDragStart = () => {
        setIsDragging(true);
    };




    return (
        <Box>
            <Typography variant="h4" component="h2" sx={{ mb: 2 }}>
                Agent Configuration
            </Typography>

            <DragDropContext onDragEnd={handleOnDragEnd} onDragStart={handleOnDragStart}>
                <Droppable droppableId="agents">

                    {(provided) => (
                        <List {...provided.droppableProps} ref={provided.innerRef}>
                            {agents.map((agent, index) => (
                              <Draggable key={agent.id} draggableId={agent.id.toString()} index={index}>  {/* Convert agent.id to string for react-beautiful-dnd */}


                                {(provided) => (
                                    <ListItem 
                                      {...provided.draggableProps}
                                      {...provided.dragHandleProps}
                                      ref={provided.innerRef}
                                      sx={{ border: isDragging ? '1px solid grey' : 'none' }}
                                      secondaryAction={ // Put action buttons on the right.
                                        <ListItemSecondaryAction> 
                                          <IconButton edge="end" aria-label="edit" onClick={() => handleOpenEditDialog(agent)}>
                                            <EditIcon />
                                          </IconButton>
                                          <IconButton edge="end" aria-label="delete" onClick={() => handleTerminateAgent(agent.id)}>
                                            <DeleteIcon />
                                          </IconButton>
                                        </ListItemSecondaryAction>
                                      }
                                    >
                                        <ListItemText primary={agent.name} secondary={`Skills: ${agent.skills.join(', ')}`} />
                                        <FormGroup> {/*Status switch. */}
                                            <FormControlLabel
                                                control={<Switch checked={agent.status === 'active'} onChange={(e) => handleAgentStatusChange(agent.id, e.target.checked ? 'active' : 'inactive')} />}
                                                label="Active"
                                            />
                                        </FormGroup>

                                    </ListItem>
                                )}
                              </Draggable>

                            ))}
                            {provided.placeholder}
                        </List>
                    )}

                </Droppable>
            </DragDropContext>



            <Dialog open={editOpen} onClose={handleCloseEditDialog}>  {/*Edit dialog.  Replace Dialog with your UI library's modal or dialog if necessary. */}
                <DialogTitle>Edit Agent</DialogTitle>
                <DialogContent>

                    <TextField  //Input for agent name.
                        autoFocus
                        margin="dense"
                        name="name"
                        label="Name"
                        type="text"
                        fullWidth
                        variant="standard"
                        value={editedAgent?.name || ''}
                        onChange={handleInputChange}
                    />


                    <TextField //Input for agent description.
                        margin="dense"
                        name="description"
                        label="Description"
                        type="text"
                        fullWidth
                        variant="standard"
                        value={editedAgent?.description || ''}
                        onChange={handleInputChange}
                    />


                    {editedAgent?.skills.map((skill, index) => (  //Input for skills.
                        <TextField
                            key={index}
                            margin="dense"
                            name={`skill-${index}`}
                            label={`Skill ${index + 1}`}
                            type="text"
                            fullWidth
                            variant="standard"
                            value={skill}
                            onChange={(e) => handleSkillChange(e, index)}

                        />

                    ))}


                    <Button onClick={handleAddSkill}>Add Skill</Button> {/*Button to add skills. */}


                    <FormControl fullWidth sx={{ mt: 2 }}>
                        <InputLabel id="role-label">Role</InputLabel>
                        <Select
                            labelId="role-label"
                            id="role"
                            name="role"
                            value={editedAgent?.role || ''}
                            label="Role"
                            onChange={handleRoleChange}

                        >
                            <MenuItem value="admin">Admin</MenuItem>
                            <MenuItem value="analyst">Analyst</MenuItem>
                            <MenuItem value="researcher">Researcher</MenuItem>
                            {/* ... other roles ... */}
                        </Select>
                    </FormControl>



                    <Box sx={{ mt: 2 }}>  {/*Permissions checkboxes. */}
                        <Typography variant="subtitle1" sx={{ mb: 1 }}>Permissions:</Typography>
                        <FormControlLabel
                            control={<Checkbox checked={editedAgent?.permissions?.read || false} onChange={handlePermissionChange} name="read" />}
                            label="Read Data"

                        />
                        <FormControlLabel
                            control={<Checkbox checked={editedAgent?.permissions?.write || false} onChange={handlePermissionChange} name="write" />}
                            label="Write Data"

                        />

                        {/* ... more permissions ... */}

                    </Box>


                    <FormControl fullWidth sx={{ mt: 2 }}> {/*Multiselect for tools. */}
                        <InputLabel id="tools-label">Tools</InputLabel>
                        <Select
                            labelId="tools-label"
                            id="tools"
                            multiple  // Multi-select is important
                            value={editedAgent?.tools || []}
                            label="Tools"  //Update the tools list as needed.
                            onChange={handleToolChange}
                            renderValue={(selected) => selected.join(', ')}
                            name="tools"
                        >
                            <MenuItem value="Web Search">Web Search</MenuItem>
                            <MenuItem value="Local Document Search">Local Document Search</MenuItem>
                            <MenuItem value="Code Interpreter">Code Interpreter</MenuItem>
                            {/* ... other tools ... */}

                        </Select>
                    </FormControl>
                </DialogContent>



                <DialogActions>
                    <Button onClick={handleCloseEditDialog}>Cancel</Button>
                    <Button onClick={handleEditSubmit}>Save Changes</Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};


export default AgentConfigurationUI;