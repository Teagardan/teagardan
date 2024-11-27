import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import {
  fetchTasks,
  addTask,
  updateTask,
  deleteTask,
  selectTasks,
  selectTaskById
} from '../redux/taskSlice'; // Redux interaction
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd'; // For drag and drop
import {
  Box,
  Button,
  Typography,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  List,
  ListItem,
  ListItemText,
  IconButton,
} from '@mui/material'; // Or your UI components
import DeleteIcon from '@mui/icons-material/Delete'; // Example delete icon (MUI)
import EditIcon from '@mui/icons-material/Edit';   // Example edit icon (MUI)
import { v4 as uuidv4 } from 'uuid';  //For generating unique task IDs.


const TaskManagerUI = () => {
    const dispatch = useDispatch();
    const tasks = useSelector(selectTasks); // Accessing the tasks state using Redux.
    const agents = useSelector(state => state.agents.agents); // You'll need agents to assign tasks


    const [newTaskDialogOpen, setNewTaskDialogOpen] = useState(false);
    const [editTaskDialogOpen, setEditTaskDialogOpen] = useState(false);
    const [newTask, setNewTask] = useState({ description: '', agentId: '', status: 'pending', priority: 'medium', id: uuidv4()});  //New task state
    const [editedTask, setEditedTask] = useState(null);  //State for the task being edited.

    useEffect(() => {
        dispatch(fetchTasks());
    }, [dispatch]);


    const handleOnDragEnd = (result) => {
      if (!result.destination) return; //No changes if dropped outside.

      const items = Array.from(tasks);
      const [reorderedItem] = items.splice(result.source.index, 1);
      items.splice(result.destination.index, 0, reorderedItem);

      // Dispatch an action to update the tasks' order on the server.
      // Implement backend logic to save order if needed. (not implemented here).
    }


    const handleAddTask = () => {
      setNewTask({ description: '', agentId: '', status: 'pending', priority: 'medium', id: uuidv4()}); // Initialize newTask with UUID
      setNewTaskDialogOpen(true);
    };



    const handleNewTaskDialogClose = () => {
        setNewTaskDialogOpen(false);
    };



    const handleNewTaskSubmit = async () => {
        try {

            await dispatch(addTask(newTask)).unwrap();
            setNewTaskDialogOpen(false);
        } catch (error) {
            console.error("Error adding task:", error);
            alert(error.response ? error.response.data.error : error.message);
        }

    };


    const handleEditTask = (task) => {  //Opens edit dialog and initializes editedTask state.
      setEditedTask({ ...task });
      setEditTaskDialogOpen(true);
    };



    const handleEditTaskDialogClose = () => {  //Close dialog
        setEditedTask(null);
        setEditTaskDialogOpen(false);

    };



    const handleEditTaskSubmit = async () => { //Handles submitting changes.
      try {
        await dispatch(updateTask(editedTask)).unwrap(); //Dispatch the updated task.
        setEditTaskDialogOpen(false);

    } catch (error) {
        console.error("Error updating task:", error);
        alert(error.response ? error.response.data.error : error.message);
    }
    };

    const handleDeleteTask = async (taskId) => {  //Deletes task from Redux and makes API call.
        try {
            await dispatch(deleteTask(taskId)).unwrap();

        } catch (error) {
            console.error("Error deleting task:", error);
            alert(error.response ? error.response.data.error : error.message);
        }
    };



    const handleInputChange = (e, field) => {  //Generic change handler for new/edit tasks.
        if (field === 'newTask') {

            setNewTask({ ...newTask, [e.target.name]: e.target.value });  
        } else {

            setEditedTask({ ...editedTask, [e.target.name]: e.target.value });  
        }
    };



    return (
        <div>
            {/* New Task Dialog */}
            <Dialog open={newTaskDialogOpen} onClose={handleNewTaskDialogClose}>  {/*Modify for your UI library as needed.*/}
                <DialogTitle>Add New Task</DialogTitle>
                <DialogContent>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="description"
                        label="Task Description"
                        type="text"
                        fullWidth
                        variant="standard"
                        name="description"  //Add name attribute
                        value={newTask.description}
                        onChange={(e) => handleInputChange(e, 'newTask')}  //Pass 'newTask' to handler
                    />
                    <FormControl fullWidth sx={{ mt: 2 }}> {/* Agent selection */}
                        <InputLabel id="agentId-label">Agent</InputLabel>
                        <Select
                            labelId="agentId-label"
                            id="agentId"
                            name="agentId" // Name attribute for controlled component
                            value={newTask.agentId}
                            label="Agent"
                            onChange={(e) => handleInputChange(e, 'newTask')}
                        >
                            {agents.map((agent) => (
                                <MenuItem key={agent.id} value={agent.id}>{agent.name}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>


                    {/* ... other fields (status, priority, etc.) ... */}

                </DialogContent>
                <DialogActions>
                    <Button onClick={handleNewTaskDialogClose}>Cancel</Button>
                    <Button onClick={handleNewTaskSubmit}>Submit</Button>
                </DialogActions>
            </Dialog>





            {/* Edit Task Dialog */}
            <Dialog open={editTaskDialogOpen} onClose={handleEditTaskDialogClose}>
              <DialogTitle>Edit Task</DialogTitle>
              <DialogContent>
                <TextField
                  autoFocus
                  margin="dense"
                  id="edit-description"
                  label="Description"
                  type="text"
                  fullWidth
                  variant="standard"
                  name="description"
                  value={editedTask?.description || ''}
                  onChange={(e) => handleInputChange(e, 'editedTask')}

                />
                <FormControl fullWidth sx={{ mt: 2 }}> {/* Agent selection */}
                  <InputLabel id="edit-agent-label">Agent</InputLabel>
                  <Select
                    labelId="edit-agent-label"
                    id="edit-agent"
                    variant="standard"
                    name="agentId"
                    label="Agent"
                    value={editedTask?.agentId || ''}
                    onChange={(e) => handleInputChange(e, 'editedTask')}
                  >
                    {agents.map((agent) => (
                      <MenuItem key={agent.id} value={agent.id}>{agent.name}</MenuItem>
                    ))}
                  </Select>
                </FormControl>


                {/* ... other fields for editing ... */}

              </DialogContent>
              <DialogActions>
                <Button onClick={handleEditTaskDialogClose}>Cancel</Button>
                <Button onClick={handleEditTaskSubmit}>Submit</Button>
              </DialogActions>
            </Dialog>





            <Typography variant="h5" component="h2">Task Manager</Typography>  {/*Example title. */}
            <Button variant="contained" onClick={handleAddTask}>Add Task</Button>

            <DragDropContext onDragEnd={handleOnDragEnd}> {/*For drag and drop. */}
                <Droppable droppableId="tasks">
                    {(provided) => (
                      <List {...provided.droppableProps} ref={provided.innerRef}>
                        {tasks.map((task, index) => (
                          <Draggable key={task.id} draggableId={task.id} index={index}> {/*Unique task ID as key */}

                            {(provided) => (
                              <ListItem
                                {...provided.draggableProps}
                                {...provided.dragHandleProps}
                                ref={provided.innerRef}
                              >
                                <ListItemText
                                  primary={task.description}
                                  secondary={`Agent: ${agents.find(a => a.id === task.agentId)?.name || 'Unassigned'}, Status: ${task.status}, Priority: ${task.priority}`}
                                />
                                <IconButton edge="end" aria-label="edit" onClick={() => handleEditTask(task)}>
                                  <EditIcon />
                                </IconButton>
                                <IconButton edge="end" aria-label="delete" onClick={()=> handleDeleteTask(task.id)}>
                                  <DeleteIcon />
                                </IconButton>
                              </ListItem>
                            )}
                          </Draggable>

                        ))}
                        {provided.placeholder} {/*Placeholder for droppable*/}

                      </List>
                    )}
                </Droppable>
            </DragDropContext>



        </div>
    );
};


export default TaskManagerUI;