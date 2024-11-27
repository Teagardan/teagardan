import React, { useEffect, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useParams } from 'react-router-dom';
import { sendMessage, selectMessagesByAgentId } from '../redux/messageSlice'; //Redux actions/selectors
import {
    List,
    ListItem,
    ListItemText,
    Typography,
    TextField,
    Button,
    Box
} from '@mui/material'; //Or your UI library.


const Thread = () => {
    const { id } = useParams(); // Get agent ID from route parameters
    const dispatch = useDispatch();
    const messages = useSelector(state => selectMessagesByAgentId(state, id)); // Get messages from Redux store using selector.
    const [newMessage, setNewMessage] = useState('');
    const messagesEndRef = useRef(null);  // For auto-scrolling



    useEffect(() => {
      // Scroll to bottom when messages update:
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);



    const handleSendMessage = async () => {
        if (newMessage.trim() === '') return;  //Don't send empty messages.

        dispatch(sendMessage({ agentId: id, text: newMessage })); //Dispatch sendMessage action.
        setNewMessage(''); // Clear the input field.
    };

    // If agent was not found, show appropriate message:
    if (!messages) {
        return (
            <div>
                <Typography variant="h6">Agent not found or no conversation history.</Typography>
            </div>
        );
    }



    return (
        <Box> {/*Use Box for styling flexbox. */}
            <Typography variant="h5" component="h2">
                Thread 
            </Typography>

            <List>
                {messages.map((message) => (
                    <ListItem key={message.id}> {/*Give unique IDs to messages in Redux store. */}
                        <ListItemText primary={message.text} secondary={message.agent} />
                    </ListItem>
                ))}
                <div ref={messagesEndRef} /> {/* For scrolling to bottom */}

            </List>

            <TextField 
              label="Enter message"
              variant="outlined"
              fullWidth  //Take up full width.
              value={newMessage}
              onChange={e=> setNewMessage(e.target.value)}
              onKeyDown={e => {  //Handles pressing enter to send.
                  if (e.key === 'Enter') {
                      handleSendMessage();
                  }
                }}
            />

            <Button variant="contained" color="primary" onClick={handleSendMessage} sx={{ mt: 2 }}>Send</Button>
        </Box>
    );

};


export default Thread;