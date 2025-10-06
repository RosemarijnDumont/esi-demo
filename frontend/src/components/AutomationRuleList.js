// frontend/src/components/AutomationRuleList.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Box, Typography, Button, List, ListItem, ListItemText, ListItemSecondaryAction, IconButton,
  Paper, TextField, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';

function AutomationRuleList() {
  const [rules, setRules] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [ruleToDelete, setRuleToDelete] = useState(null);

  useEffect(() => {
    fetchRules();
  }, []);

  const fetchRules = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/rules');
    const data = await response.json();
    setRules(data);
  };

  const handleDeleteClick = (rule) => {
    setRuleToDelete(rule);
    setOpenDeleteDialog(true);
  };

  const handleConfirmDelete = async () => {
    if (ruleToDelete) {
      await fetch(`http://127.0.0.1:5000/api/rules/${ruleToDelete.id}`, {
        method: 'DELETE',
      });
      fetchRules();
      setOpenDeleteDialog(false);
      setRuleToDelete(null);
    }
  };

  const handleCloseDeleteDialog = () => {
    setOpenDeleteDialog(false);
    setRuleToDelete(null);
  };

  const filteredRules = rules.filter(rule =>
    rule.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Automation Rules</Typography>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <TextField
          label="Search Rules"
          variant="outlined"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ width: '300px' }}
        />
        <Button
          variant="contained"
          color="primary"
          component={Link}
          to="/rules/new"
          startIcon={<AddIcon />}
        >
          Create New Rule
        </Button>
      </Box>
      <Paper elevation={2} sx={{ mt: 3 }}>
        <List>
          {filteredRules.map((rule) => (
            <ListItem
              key={rule.id}
              disableGutters
              sx={{ borderBottom: '1px solid #eee' }}
            >
              <ListItemText
                primary={rule.name}
                secondary={
                  <>
                    <Typography component="span" variant="body2" color="text.primary">
                      Conditions: {JSON.stringify(rule.conditions)}
                    </Typography>
                    <br/>
                    <Typography component="span" variant="body2" color="text.primary">
                      Actions: {JSON.stringify(rule.actions)}
                    </Typography>
                    <br/>
                    <Typography component="span" variant="body2" color="text.secondary">
                      Priority: {rule.priority} | Status: {rule.is_active ? 'Active' : 'Inactive'}
                    </Typography>
                  </>
                }
              />
              <ListItemSecondaryAction>
                <IconButton edge="end" aria-label="edit" component={Link} to={`/rules/edit/${rule.id}`}>
                  <EditIcon />
                </IconButton>
                <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteClick(rule)}>
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
            Are you sure you want to delete the rule "{ruleToDelete?.name}"? This action cannot be undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDeleteDialog}>Cancel</Button>
          <Button onClick={handleConfirmDelete} autoFocus color="error">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default AutomationRuleList;
