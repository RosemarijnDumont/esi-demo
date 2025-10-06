// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Button, Container, Box } from '@mui/material';
import EmailTemplateList from './components/EmailTemplateList';
import EmailTemplateForm from './components/EmailTemplateForm';
import AutomationRuleList from './components/AutomationRuleList';
import AutomationRuleForm from './components/AutomationRuleForm';
import AnalyticsDashboard from './components/AnalyticsDashboard';

function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Automated Email System
          </Typography>
          <Button color="inherit" component={Link} to="/">Templates</Button>
          <Button color="inherit" component={Link} to="/rules">Rules</Button>
          <Button color="inherit" component={Link} to="/analytics">Analytics</Button>
        </Toolbar>
      </AppBar>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Routes>
          <Route path="/" element={<EmailTemplateList />} />
          <Route path="/templates/new" element={<EmailTemplateForm />} />
          <Route path="/templates/edit/:id" element={<EmailTemplateForm />} />
          <Route path="/rules" element={<AutomationRuleList />} />
          <Route path="/rules/new" element={<AutomationRuleForm />} />
          <Route path="/rules/edit/:id" element={<AutomationRuleForm />} />
          <Route path="/analytics" element={<AnalyticsDashboard />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;
