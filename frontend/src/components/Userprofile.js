import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { updateUser, deleteUser, selectUser } from '../redux/userSlice'; // Redux integration
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  TextField,
  Button,
  Avatar, // For profile pictures
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
} from '@mui/material'; // Or your UI library


const UserProfile = ({ onLogout }) => {  // Receives onLogout prop
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const user = useSelector(selectUser);
    const [editOpen, setEditOpen] = useState(false); // State for the edit dialog
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false); // State for delete confirmation dialog
    const [editedUser, setEditedUser] = useState({ ...user }); // State for editing user data

    useEffect(() => { // Update editedUser whenever user data changes in Redux.
        setEditedUser({ ...user });
    }, [user]);



    const handleEditOpen = () => {
        setEditOpen(true);
    };


    const handleEditClose = () => {
        setEditedUser({ ...user });  //Reset to stored values
        setEditOpen(false);

    };

    const handleEditSubmit = async () => {  //Dispatch action to update user profile
      try {
        await dispatch(updateUser(editedUser)).unwrap();

        setEditOpen(false);
    } catch (error) {
        console.error("Error updating profile:", error);
        alert(error.response ? error.response.data.error : error.message);
    }
    };



    const handleDeleteOpen = () => {
      setDeleteDialogOpen(true);

    };


    const handleDeleteClose = () => {
        setDeleteDialogOpen(false);
    };



    const handleDeleteConfirm = async () => { //Dispatch action to delete user, then redirect to login.
        try {
            await dispatch(deleteUser()).unwrap(); // Redux action

            onLogout(); //Call logout handler from props
            navigate('/login');  // Redirect

        } catch (error) {
            console.error("Error deleting profile:", error);
            alert(error.response ? error.response.data.error : error.message);
        }

    };



    const handleInputChange = (e) => {  //Handles changes in edit form
        setEditedUser({...editedUser, [e.target.name]: e.target.value });

    };



    return (
        <Box sx={{ p: 2 }}> {/*Outer container for padding. */}
            <Typography variant="h4" component="h2" gutterBottom>User Profile</Typography>

            <Avatar alt={user.name} src={user.profilePicture} sx={{ width: 100, height: 100, mb: 2 }} /> {/*If you're using avatars. */}


            {/*If the user has an avatar, display it here.  You would likely store the URL of the avatar in your Redux store. */}



            <Typography variant="body1">Name: {user.name}</Typography>  {/*User's name. */}
            <Typography variant="body1">Email: {user.email}</Typography>  {/*User's email. */}

            {/* ... other user details ... */} {/*Add other details if applicable (e.g., username, roles, etc.). */}


            <Box sx={{ mt: 2 }}>
                <Button variant="outlined" onClick={handleEditOpen} startIcon={<EditIcon />}>Edit Profile</Button> {/*Button to open edit profile dialog */}
                <Button variant="outlined" color="error" onClick={handleDeleteOpen} startIcon={<DeleteIcon />} sx={{ ml: 2 }}>Delete Account</Button> {/*Button to open delete confirmation. */}
            </Box>


            <Dialog open={editOpen} onClose={handleEditClose}> {/*Edit dialog, implement Dialog for your UI library or framework. */}
                <DialogTitle>Edit Profile</DialogTitle>
                <DialogContent>
                    <TextField autoFocus margin="dense" id="name" name="name" label="Name" type="text" fullWidth variant="standard" value={editedUser.name} onChange={handleInputChange}/>
                    <TextField margin="dense" id="email" name="email" label="Email" type="email" fullWidth variant="standard" value={editedUser.email} onChange={handleInputChange}/>
                    {/* ... input fields for other editable details ... */} {/*Add other input fields if needed. */}

                </DialogContent>
                <DialogActions>

                    <Button onClick={handleEditClose}>Cancel</Button>
                    <Button onClick={handleEditSubmit}>Save Changes</Button>
                </DialogActions>

            </Dialog>


            <Dialog  //Delete confirmation dialog
                open={deleteDialogOpen}
                onClose={handleDeleteClose}
                aria-labelledby="alert-dialog-title"
                aria-describedby="alert-dialog-description"
            >
                <DialogTitle id="alert-dialog-title">{"Confirm Account Deletion"}</DialogTitle>
                <DialogContent>

                    <DialogContentText id="alert-dialog-description">Are you sure you want to delete your account? This action cannot be undone.
                    </DialogContentText>
                </DialogContent>

                <DialogActions>
                    <Button onClick={handleDeleteClose}>Cancel</Button>
                    <Button onClick={handleDeleteConfirm} autoFocus color="error">Delete Account</Button>
                </DialogActions>
            </Dialog>


            <Button variant="outlined" color="secondary" onClick={onLogout} sx={{ mt: 2 }}>Logout</Button>
        </Box>
    );

};



export default UserProfile;