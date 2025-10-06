// frontend/src/components/EmailTemplateForm.js
import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { 
  Box, Typography, TextField, Button, Paper, FormControlLabel, Switch, MenuItem, Select, InputLabel, FormControl 
} from '@mui/material';

function EmailTemplateForm() {
  const [name, setName] = useState('');
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [isActive, setIsActive] = useState(true);
  const [statusMessage, setStatusMessage] = useState('');
  const navigate = useNavigate();
  const { id } = useParams(); // For editing existing templates

  useEffect(() => {
    if (id) {
      // Fetch template data for editing
      const fetchTemplate = async () => {
        const response = await fetch(`http://127.0.0.1:5000/api/templates/${id}`);
        const data = await response.json();
        setName(data.name);
        setSubject(data.subject);
        setBody(data.body);
        setIsActive(data.is_active);
      };
      fetchTemplate();
    }
  }, [id]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setStatusMessage('');

    const templateData = { name, subject, body, is_active: isActive };
    const method = id ? 'PUT' : 'POST';
    const url = id ? `http://127.0.0.1:5000/api/templates/${id}` : 'http://127.0.0.1:5000/api/templates';

    try {
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(templateData),
      });

      if (response.ok) {
        setStatusMessage(`Template ${id ? 'updated' : 'created'} successfully!`);
        setTimeout(() => navigate('/'), 1500); // Redirect after a short delay
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
      <Typography variant="h4" gutterBottom>{id ? 'Edit Email Template' : 'Create New Email Template'}</Typography>
      <Paper elevation={2} sx={{ p: 4 }}>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Template Name"
            variant="outlined"
            fullWidth
            value={name}
            onChange={(e) => setName(e.target.value)}
            margin="normal"
            required
            disabled={!!id} // Disable name edit for existing templates
          />
          <TextField
            label="Subject"
            variant="outlined"
            fullWidth
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            margin="normal"
            required
          />
          <TextField
            label="Body (supports Markdown)"
            variant="outlined"
            fullWidth
            multiline
            rows={10}
            value={body}
            onChange={(e) => setBody(e.target.value)}
            margin="normal"
            required
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
          
          {/* Placeholder for Version Control/Approval Workflow components */}
          {id && (
            <Box sx={{ mt: 3, p: 2, border: '1px dashed #ccc', borderRadius: 1 }}>
              <Typography variant="subtitle1" gutterBottom>Approval Workflow & Version Control (Future Implementation)</Typography>
              <Typography variant="body2" color="text.secondary">Current Status: Pending Review | Last Approved: v{/* Fetch actual version */}
              </Typography>
              {/* Example: A dropdown for 'Request Approval' / 'Approve' actions */}
              <FormControl fullWidth margin="normal" disabled>
                <InputLabel>Action</InputLabel>
                <Select
                  value="none"
                  label="Action"
                >
                  <MenuItem value="none">No action</MenuItem>
                  <MenuItem value="request_review">Request Review</MenuItem>
                  <MenuItem value="approve">Approve Changes</MenuItem>
                  <MenuItem value="reject">Reject Changes</MenuItem>
                </Select>
              </FormControl>
            </Box>
          )}

          <Button 
            type="submit" 
            variant="contained" 
            color="primary" 
            sx={{ mt: 3, mr: 2 }}
          >
            {id ? 'Update Template' : 'Create Template'}
          </Button>
          <Button 
            type="button" 
            variant="outlined" 
            sx={{ mt: 3 }}
            onClick={() => navigate('/')}
          >
            Cancel
          </Button>
          {statusMessage && <Typography sx={{ mt: 2, color: response => response.ok ? 'success.main' : 'error.main' }}>{statusMessage}</Typography>}
        </form>
      </Paper>
    </Box>
  );
}

export default EmailTemplateForm;
