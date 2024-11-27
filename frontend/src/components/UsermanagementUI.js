import React, { useState, useEffect, useCallback } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchUsers,
  createUser,
  updateUser,
  deleteUser,
  selectUsers,
} from '../redux/usersSlice'; // Redux integration
import {
  Box,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper, // For table styling
  IconButton,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material'; // Import UI components (replace with your UI library)
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete'; //For delete icon.


const UserManagementUI = () => {
    const dispatch = useDispatch();
    const users = useSelector(selectUsers); // Access users from Redux store
    const [createUserDialogOpen, setCreateUserDialogOpen] = useState(false);
    const [editUserDialogOpen, setEditUserDialogOpen] = useState(false);
    const [newUser, setNewUser] = useState({ name: '', email: '', role: '' }); // New user state
    const [editedUser, setEditedUser] = useState(null); // State for editing user data



    useEffect(() => {
        dispatch(fetchUsers());
    }, [dispatch]);




    const handleCreateUserOpen = () => {
        setNewUser({ name: '', email: '', role: '' }); // Reset form fields
        setCreateUserDialogOpen(true);
    };



    const handleCreateUserClose = () => {
        setCreateUserDialogOpen(false);
    };





    const handleCreateUserSubmit = async () => {
        try {
            await dispatch(createUser(newUser)).unwrap();

            setCreateUserDialogOpen(false);  //Close form after creation.
        } catch (error) {
            console.error('Error creating user:', error);
            // Optionally display error message to user with:  alert(error.message);
            alert(error.response ? error.response.data.error : error.message);
        }
    };



    const handleEditUserOpen = (user) => {
        setEditedUser({ ...user }); // Set editedUser state with the user's data
        setEditUserDialogOpen(true);
    };




    const handleEditUserClose = () => {  //Closes the edit dialog.
        setEditUserDialogOpen(false);

    };



    const handleEditUserSubmit = async () => {
        try {
            await dispatch(updateUser(editedUser)).unwrap(); //Dispatch updateUser action with changed user data

            setEditUserDialogOpen(false);

        } catch (error) {
            console.error('Error updating user:', error);
            // Handle the error, such as by displaying an error message
            alert(error.response ? error.response.data.error : error.message);
        }

    };



    const handleDeleteUser = async (userId) => {
        try {
          await dispatch(deleteUser(userId)).unwrap();  //Dispatch Redux action.


        } catch (error) {
            console.error("Error deleting user:", error);
            // Handle the error, such as by displaying an error message
            alert(error.response ? error.response.data.error : error.message);
        }

    };




    const handleInputChange = (e, field) => {
        const { name, value } = e.target;
        if (field === 'newUser') {
            setNewUser(prevState => ({ ...prevState, [name]: value }));  //For new users.
        } else {
            setEditedUser(prevState => ({ ...prevState, [name]: value })); //For editing existing users

        }
    };



    return (
        <Box sx={{ padding: 2 }}>
            {/* ... other JSX ... */}  {/*Add Typography or other components as needed. */}
            <Typography variant="h4" component="h2" gutterBottom>User Management</Typography>
            <Button onClick={handleCreateUserOpen} variant="contained" color="primary">Create User</Button>  {/*Button to open create user dialog. */}


            <TableContainer component={Paper}> {/*Use TableContainer if needed. */}
                <Table>
                  <TableHead> {/*Table header */}
                    <TableRow>
                      <TableCell>Name</TableCell> {/*Customize columns */}
                      <TableCell>Email</TableCell>
                      <TableCell>Role</TableCell>
                      <TableCell></TableCell> {/*For edit/delete buttons. */}

                    </TableRow>
                  </TableHead>
                    <TableBody>

                        {users.map((user) => (  //Map through and render users in table.
                            <TableRow key={user.id}>  {/*Unique user ID as key. */}
                                <TableCell component="th" scope="row">{user.name}</TableCell>
                                <TableCell>{user.email}</TableCell>
                                <TableCell>{user.role}</TableCell>
                                <TableCell align="right"> {/*Edit and Delete buttons */}
                                    <IconButton aria-label="edit" onClick={() => handleEditUserOpen(user)} color="primary">
                                        <EditIcon />
                                    </IconButton>
                                    <IconButton aria-label="delete" onClick={() => handleDeleteUser(user.id)} color="error">
                                      <DeleteIcon />
                                    </IconButton>
                                </TableCell>

                            </TableRow>
                        ))}
                    </TableBody>

                </Table>

            </TableContainer>


          <Dialog open={createUserDialogOpen} onClose={handleCreateUserClose}>  {/*Dialog for creating a user, replace with your preferred UI library's Dialog or modal. */}
            <DialogTitle>Create New User</DialogTitle>
            <DialogContent>
              <TextField
                autoFocus
                margin="dense"
                id="name"
                label="Name"
                type="text"
                fullWidth
                variant="standard"
                name="name"
                value={newUser.name}
                onChange={(e) => handleInputChange(e, 'newUser')}
              />
              <TextField
                margin="dense"
                id="email"
                label="Email Address"
                type="email"
                fullWidth
                variant="standard"
                name="email"
                value={newUser.email}
                onChange={(e) => handleInputChange(e, 'newUser')}

              />
              <FormControl fullWidth sx={{ mt: 2 }}>
                <InputLabel id="role-label">Role</InputLabel>
                <Select
                  labelId="role-label"
                  id="role"
                  name="role"  // Add name attribute
                  value={newUser.role}
                  label="Role"
                  onChange={(e) => handleInputChange(e, 'newUser')}

                >
                  <MenuItem value="admin">Admin</MenuItem>  {/* Add more roles as needed. */}
                  <MenuItem value="user">User</MenuItem>
                  {/* ... more roles ... */}
                </Select>
              </FormControl>
              {/* ... Other user creation inputs ... */}

            </DialogContent>

            <DialogActions>
              <Button onClick={handleCreateUserClose}>Cancel</Button>
              <Button onClick={handleCreateUserSubmit}>Create</Button>
            </DialogActions>

          </Dialog>

          {/*Edit User dialog.  */}
          <Dialog open={editUserDialogOpen} onClose={handleEditUserClose}>  {/*Dialog for editing users.  Replace with your preferred UI framework or library. */}

              <DialogTitle>Edit User</DialogTitle>
              <DialogContent>

                  <TextField
                      autoFocus
                      margin="dense"
                      id="edit-name"
                      label="Name"
                      type="text"
                      fullWidth
                      variant="standard"
                      name="name"
                      value={editedUser?.name || ''} // Handle undefined for initial render
                      onChange={(e) => handleInputChange(e, 'editedUser')} // Use editedUser for existing users
                  />

                  <TextField  //Input field for email.
                      margin="dense"
                      id="edit-email"
                      label="Email Address"
                      type="email"
                      fullWidth
                      variant="standard"
                      name="email"
                      value={editedUser?.email || ''}
                      onChange={(e) => handleInputChange(e, 'editedUser')}
                  />

                  <FormControl fullWidth sx={{ mt: 2 }}>
                      <InputLabel id="edit-role-label">Role</InputLabel>
                      <Select
                          labelId="edit-role-label"
                          id="edit-role"
                          name="role"  // Add name attribute
                          value={editedUser?.role || ''}  // Handle undefined initial values
                          label="Role"
                          onChange={(e) => handleInputChange(e, 'editedUser')}
                      >
                          <MenuItem value="admin">Admin</MenuItem> {/* Add more role options. */}
                          <MenuItem value="user">User</MenuItem>

                          {/* ... more roles ... */}
                      </Select>
                  </FormControl>
              </DialogContent>

              <DialogActions> {/*Buttons for edit user dialog */}

                  <Button onClick={handleEditUserClose}>Cancel</Button>
                  <Button onClick={handleEditUserSubmit}>Save</Button>
              </DialogActions>
          </Dialog>



        </Box>
    );
};


export default UserManagementUI;