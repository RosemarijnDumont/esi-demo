// frontend/src/components/EmailTemplateList.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  Box, Typography, Button, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, 
  Paper, TextField, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle 
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import AddIcon from '@mui/icons-material/Add';
import ReactMarkdown from 'react-markdown';

function EmailTemplateList() {
  const [templates, setTemplates] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [templateToDelete, setTemplateToDelete] = useState(null);
  const [openPreviewDialog, setOpenPreviewDialog] = useState(false);
  const [templateToPreview, setTemplateToPreview] = useState(null);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/templates');
    const data = await response.json();
    setTemplates(data);
  };

  const handleDeleteClick = (template) => {
    setTemplateToDelete(template);
    setOpenDeleteDialog(true);
  };

  const handleConfirmDelete = async () => {
    if (templateToDelete) {
      await fetch(`http://127.0.0.1:5000/api/templates/${templateToDelete.id}`, {
        method: 'DELETE',
      });
      fetchTemplates();
      setOpenDeleteDialog(false);
      setTemplateToDelete(null);
    }
  };

  const handleCloseDeleteDialog = () => {
    setOpenDeleteDialog(false);
    setTemplateToDelete(null);
  };

  const handlePreviewClick = (template) => {
    setTemplateToPreview(template);
    setOpenPreviewDialog(true);
  };

  const handleClosePreviewDialog = () => {
    setOpenPreviewDialog(false);
    setTemplateToPreview(null);
  };

  const filteredTemplates = templates.filter(template =>
    template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    template.subject.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Email Templates</Typography>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <TextField
          label="Search Templates"
          variant="outlined"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ width: '300px' }}
        />
        <Button 
          variant="contained" 
          color="primary" 
          component={Link} 
          to="/templates/new"
          startIcon={<AddIcon />}
        >
          Create New Template
        </Button>
      </Box>
      <Paper elevation={2} sx={{ mt: 3 }}>
        <List>
          {filteredTemplates.map((template) => (
            <ListItem
              key={template.id}
              disableGutters
              sx={{ borderBottom: '1px solid #eee' }}
            >
              <ListItemText 
                primary={template.name}
                secondary={
                  <>
                    <Typography component="span" variant="body2" color="text.primary">
                      Subject: {template.subject}
                    </Typography>
                    <br/>
                    <Typography component="span" variant="body2" color="text.secondary">
                      Version: {template.version} | Status: {template.is_active ? 'Active' : 'Inactive'}
                    </Typography>
                  </>
                }
              />
              <ListItemSecondaryAction>
                <IconButton edge="end" aria-label="preview" onClick={() => handlePreviewClick(template)}>
                  <VisibilityIcon />
                </IconButton>
                <IconButton edge="end" aria-label="edit" component={Link} to={`/templates/edit/${template.id}`}>
                  <EditIcon />
                </IconButton>
                <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteClick(template)}>
                  <DeleteIcon />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
      </Paper>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={openDeleteDialog}
        onClose={handleCloseDeleteDialog}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"Confirm Delete"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            Are you sure you want to delete the template "{templateToDelete?.name}"? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDeleteDialog}>Cancel</Button>
          <Button onClick={handleConfirmDelete} autoFocus color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Template Preview Dialog */}
      <Dialog
        open={openPreviewDialog}
        onClose={handleClosePreviewDialog}
        maxWidth="md"
        fullWidth
        aria-labelledby="preview-dialog-title"
      >
        <DialogTitle id="preview-dialog-title">Preview: {templateToPreview?.name}</DialogTitle>
        <DialogContent dividers>
          <Typography variant="h6" gutterBottom>Subject: {templateToPreview?.subject}</Typography>
          <Box sx={{ border: '1px solid #ddd', padding: 2, borderRadius: 1, maxHeight: '400px', overflowY: 'auto' }}>
            <ReactMarkdown children={templateToPreview?.body || ''} />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClosePreviewDialog}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default EmailTemplateList;
