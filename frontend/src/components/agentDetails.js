import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams, useNavigate } from 'react-router-dom';
import { updateAgent, selectAgentById } from '../redux/agentSlice'; // Import Redux actions and selectors
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogContentText,
    DialogActions,
    Button,
    TextField,
    Typography,
} from '@mui/material'; // Import UI components from your UI library


const AgentDetails = () => {
    const { id } = useParams(); // Get the agent ID from the URL parameters
    const agent = useSelector(state => selectAgentById(state, id)); // Get agent details using selector and ID from route parameter.
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const [editAgent, setEditAgent] = useState(null);  // State for editing
    const [editOpen, setEditOpen] = useState(false); // State for edit dialog


    if (!agent) {
        return (
          <div>
            <Typography variant="h6">Agent Not Found</Typography>
            <Button onClick={() => navigate('/')}>Back to Agent List</Button>
          </div>
        );
      }



    const handleEditClick = () => {
        // Set initial edit agent state when opening edit dialog:
        setEditAgent({ ...agent }); 
        setEditOpen(true); // Open the edit dialog
    };

    const handleEditClose = () => {
        setEditAgent(null);  // Clear the editing agent.
        setEditOpen(false); // Close the edit dialog
    };




    const handleEditInputChange = (e) => {
        setEditAgent({ ...editAgent, [e.target.name]: e.target.value });
    };


    const handleEditSkillChange = (e, index) => {
        const newSkills = [...editAgent.skills];
        newSkills[index] = e.target.value;
        setEditAgent({...editAgent, skills: newSkills});
    };
    

    const handleAddSkill = () => {
        setEditAgent({...editAgent, skills: [...editAgent.skills, '']});

    };


    const handleEditSubmit = async (e) => {
        e.preventDefault();
        try {
            await dispatch(updateAgent(editAgent)).unwrap(); //Dispatch update action and unwrap potential rejections.

            setEditOpen(false); // Close dialog
            navigate('/');  // Navigate back to agent list (optional)
        } catch (error) {
            console.error("Error updating agent:", error);
            // ... handle error as needed
            alert(error.response ? error.response.data.error : error.message);
        }
    };





    return (
      <div>

        <Dialog open={editOpen} onClose={handleEditClose}>
            <DialogTitle>Edit Agent</DialogTitle>
            <DialogContent>
                <TextField
                    autoFocus
                    margin="dense"
                    name="name"
                    label="Name"
                    type="text"
                    fullWidth
                    variant="standard"
                    value={editAgent ? editAgent.name : ''} // Set value from editAgent state
                    onChange={handleEditInputChange}
                />
                <TextField
                    margin="dense"
                    name="description"
                    label="Description"
                    type="text"
                    fullWidth
                    variant="standard"
                    value={editAgent ? editAgent.description : ''}
                    onChange={handleEditInputChange}
                />

                {editAgent && editAgent.skills.map((skill, index) => (
                    <TextField
                      key={index}
                      margin="dense"
                      name={`skill-${index}`}
                      label={`Skill ${index+1}`}
                      type="text"
                      fullWidth
                      variant="standard"
                      value={skill}
                      onChange={(e) => handleEditSkillChange(e, index)}
                    />
                  ))}

                <Button onClick={handleAddSkill}>Add Skill</Button>

            </DialogContent>

            <DialogActions>
                <Button onClick={handleEditClose}>Cancel</Button>
                <Button onClick={handleEditSubmit}>Submit</Button>
            </DialogActions>
        </Dialog>

        <Typography variant="h5" component="h2">Agent Details</Typography>
        <Button variant="outlined" color="secondary" size="small" onClick={()=>navigate('/')}>Back to Agent List</Button>

        {agent && (
          <div>
            <Typography>Name: {agent.name}</Typography>
            <Typography>Description: {agent.description}</Typography>
            <Typography>Skills: {agent.skills.join(', ')}</Typography>
          </div>
        )}
        <Button onClick={handleEditClick}>Edit Agent</Button>        
      </div>
    );
};



export default AgentDetails;