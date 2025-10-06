// frontend/src/components/AutomationRuleForm.js
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  Box, Typography, TextField, Button, Paper, FormControlLabel, Switch, MenuItem, Select, InputLabel, FormControl
} from '@mui/material';

function AutomationRuleForm() {
  const [name, setName] = useState('');
  const [conditions, setConditions] = useState('{}'); // Stored as stringified JSON
  const [actions, setActions] = useState('{}');     // Stored as stringified JSON
  const [isActive, setIsActive] = useState(true);
  const [priority, setPriority] = useState(1);
  const [statusMessage, setStatusMessage] = useState('');
  const navigate = useNavigate();
  const { id } = useParams();

  useEffect(() => {
    if (id) {
      const fetchRule = async () => {
        const response = await fetch(`http://127.0.0.1:5000/api/rules/${id}`);
        const data = await response.json();
        setName(data.name);
        setConditions(JSON.stringify(data.conditions, null, 2));
        setActions(JSON.stringify(data.actions, null, 2));
        setIsActive(data.is_active);
        setPriority(data.priority);
      };
      fetchRule();
    }
  }, [id]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatusMessage('');

    let parsedConditions;
    let parsedActions;
    
    try {
      parsedConditions = JSON.parse(conditions);
    } catch (e) {
      setStatusMessage("Error: Conditions must be valid JSON.");
      return;
    }

    try {
      parsedActions = JSON.parse(actions);
    } catch (e) {
      setStatusMessage("Error: Actions must be valid JSON.");
      return;
    }

    const ruleData = { 
      name, 
      conditions: parsedConditions, 
      actions: parsedActions, 
      is_active: isActive, 
      priority 
    };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `http://127.0.0.1:5000/api/rules/${id}` : 'http://127.0.0.1:5000/api/rules';

    try {
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(ruleData),
      });

      if (response.ok) {
        setStatusMessage(`Rule ${id ? 'updated' : 'created'} successfully!`);
        setTimeout(() => navigate('/rules'), 1500);
      } else {
        const errorData = await response.json();
        setStatusMessage(`Error: ${errorData.message || 'Something went wrong.'}`);
      }
    } catch (error) {
      setStatusMessage(`Network error: ${error.message}`);
    }
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>{id ? 'Edit Automation Rule' : 'Create New Automation Rule'}</Typography>
      <Paper elevation={2} sx={{ p: 4 }}>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Rule Name"
            variant="outlined"
            fullWidth
            value={name}
            onChange={(e) => setName(e.target.value)}
            margin="normal"
            required
          />
          <TextField
            label="Conditions (JSON)"
            variant="outlined"
            fullWidth
            multiline
            rows={6}
            value={conditions}
            onChange={(e) => setConditions(e.target.value)}
            margin="normal"
            required
            helperText="Enter conditions as a JSON object, e.g., {'priority': 'high', 'category': 'billing'}"
          />
          <TextField
            label="Actions (JSON)"
            variant="outlined"
            fullWidth
            multiline
            rows={6}
            value={actions}
            onChange={(e) => setActions(e.target.value)}
            margin="normal"
            required
            helperText="Enter actions as a JSON object, e.g., {'send_template': 'Welcome Email', 'assign_to': 'Support Team'}"
          />
          <TextField
            label="Priority"
            type="number"
            variant="outlined"
            fullWidth
            value={priority}
            onChange={(e) => setPriority(Math.max(1, parseInt(e.target.value) || 1))}
            margin="normal"
            required
            inputProps={{ min: 1 }}
            helperText="Rules with lower priority numbers are evaluated first."
          />
          <FormControlLabel
            control={
              <Switch
                checked={isActive}
                onChange={(e) => setIsActive(e.target.checked)}
                name="isActive"
                color="primary"
              />
            }
            label="Active"
            sx={{ mt: 2 }}
          />
          
          <Button 
            type="submit" 
            variant="contained" 
            color="primary" 
            sx={{ mt: 3, mr: 2 }}
          >
            {id ? 'Update Rule' : 'Create Rule'}
          </Button>
          <Button 
            type="button" 
            variant="outlined" 
            sx={{ mt: 3 }}
            onClick={() => navigate('/rules')}
          >
            Cancel
          </Button>
          {statusMessage && <Typography sx={{ mt: 2, color: response => response.ok ? 'success.main' : 'error.main' }}>{statusMessage}</Typography>}
        </form>
      </Paper>
    </Box>
  );
}

export default AutomationRuleForm;
