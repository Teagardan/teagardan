import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { updateSystemSettings, selectSystemSettings } from '../redux/systemSettingsSlice';
import {
  Box,
  Typography,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Grid, // Import Grid for layout
} from '@mui/material';


const SystemAdministrationUI = () => {
  const dispatch = useDispatch();
  const systemSettings = useSelector(selectSystemSettings);
  const [editedSettings, setEditedSettings] = useState(systemSettings);


  useEffect(() => {
    setEditedSettings(systemSettings);
  }, [systemSettings]);


  const handleSettingChange = (e) => {
    const { name, value, checked, type } = e.target;
    const newValue = type === 'checkbox' ? checked : value;

    setEditedSettings((prevSettings) => ({
      ...prevSettings,
      [name]: newValue,
    }));
  };



  const handleSaveSettings = async () => {
    try {
      await dispatch(updateSystemSettings(editedSettings)).unwrap();
      alert('System settings saved successfully.'); // Provide feedback
    } catch (error) {
      console.error("Error updating system settings:", error);
      alert(error.response ? error.response.data.error : error.message);
    }
  };


  const availableModels = [
    'llama3.2:3b-instruct-q8_0', 'llama3.2:7b-instruct-q8_0', 'llama3.2:13b-instruct-q8_0', 
    // ... other model options ...  Add your actual models here.
  ];



  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" component="h2" gutterBottom>System Administration</Typography>


      <Grid container spacing={2}> {/* Use Grid for layout */}

        <Grid item xs={6}> {/* Model Selection */}

          <FormControl fullWidth>
            <InputLabel id="model-select-label">LLM Model</InputLabel>
            <Select
              labelId="model-select-label"
              id="model-select"
              name="selectedModel"
              value={editedSettings.selectedModel}
              label="LLM Model"
              onChange={handleSettingChange}
            >
              {availableModels.map((model) => (
                <MenuItem key={model} value={model}>{model}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>


        <Grid item xs={6}> {/* API Key input */}
          <TextField
            fullWidth
            label="API Key"
            name="apiKey"
            value={editedSettings.apiKey || ''}  // Handle undefined initial values
            onChange={handleSettingChange}
            variant="outlined"

          />
        </Grid>

        <Grid item xs={6}> {/* Max Context Window Size */}

          <TextField
            fullWidth
            label="Max. Context Window Size"
            name="maxContextWindowSize"
            value={editedSettings.maxContextWindowSize || ''}
            onChange={handleSettingChange}
            type="number"
            variant="outlined"
            inputProps={{ min: 0 }}
          />
        </Grid>

        <Grid item xs={6}> {/* Logging Level selection */}
          <FormControl fullWidth>
            <InputLabel id="logging-level-label">Logging Level</InputLabel>
            <Select
              labelId="logging-level-label"
              id="logging-level"
              name="loggingLevel"
              value={editedSettings.loggingLevel || 'info'}
              label="Logging Level"
              onChange={handleSettingChange}

            >
              <MenuItem value="debug">Debug</MenuItem>
              <MenuItem value="info">Info</MenuItem>
              <MenuItem value="warning">Warning</MenuItem>
              <MenuItem value="error">Error</MenuItem>
              {/* ... other logging levels ... */}

            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={6}> {/* Database File Path */}
          <TextField
              fullWidth
              label="Database File Path"
              name="databaseFilePath"
              value={editedSettings.databaseFilePath || ''}
              onChange={handleSettingChange}
              variant="outlined"

          />

        </Grid>



        {/* Other system settings (add more Grid items as needed) */}

        <Grid item xs={6}>  {/* Debug Mode Toggle */}
            <FormControlLabel
              control={<Switch checked={editedSettings.debugMode} onChange={handleSettingChange} name="debugMode" />}
              label="Debug Mode"

            />

        </Grid>

        {/* Example: Enable/Disable Feature */}
        <Grid item xs={6}>
          <FormControlLabel
            control={<Switch checked={editedSettings.featureEnabled} onChange={handleSettingChange} name="featureEnabled" />}
            label="Enable Feature X"

          />

        </Grid>
      </Grid>

      <Button variant="contained" onClick={handleSaveSettings} sx={{ mt: 3 }}>Save Settings</Button>

    </Box>
  );
};

export default SystemAdministrationUI;