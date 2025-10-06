// frontend/src/components/AnalyticsDashboard.js
import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Grid, CircularProgress, Alert } from '@mui/material';
import { styled } from '@mui/material/styles';

const StatCard = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  textAlign: 'center',
  color: theme.palette.text.secondary,
  minHeight: 120,
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  alignItems: 'center',
}));

function AnalyticsDashboard() {
  const [summary, setSummary] = useState(null);
  const [templatePerformance, setTemplatePerformance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAnalyticsData = async () => {
      try {
        setLoading(true);
        const [summaryResponse, performanceResponse] = await Promise.all([
          fetch('http://127.0.0.1:5000/api/analytics/summary'),
          fetch('http://127.0.0.1:5000/api/analytics/template_performance'),
        ]);

        if (!summaryResponse.ok || !performanceResponse.ok) {
          throw new Error('Failed to fetch analytics data');
        }

        const summaryData = await summaryResponse.json();
        const performanceData = await performanceResponse.json();

        setSummary(summaryData);
        setTemplatePerformance(performanceData);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalyticsData();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 5 }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ ml: 2 }}>Loading Analytics...</Typography>
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">Error loading analytics: {error}</Alert>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Analytics Dashboard</Typography>
      
      {summary && (
        <Box mb={4}>
          <Typography variant="h5" gutterBottom>System Overview</Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard elevation={3}>
                <Typography variant="h5" color="primary">{summary.total_emails_sent}</Typography>
                <Typography variant="subtitle1">Emails Sent</Typography>
              </StatCard>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard elevation={3}>
                <Typography variant="h5" color="success.main">{summary.open_rate}</Typography>
                <Typography variant="subtitle1">Open Rate</Typography>
              </StatCard>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard elevation={3}>
                <Typography variant="h5" color="info.main">{summary.click_through_rate}</Typography>
                <Typography variant="subtitle1">Click-Through Rate</Typography>
              </StatCard>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard elevation={3}>
                <Typography variant="h5" color="error.main">{summary.bounced_emails}</Typography>
                <Typography variant="subtitle1">Bounced Emails</Typography>
              </StatCard>
            </Grid>
          </Grid>
        </Box>
      )}

      {templatePerformance.length > 0 && (
        <Box>
          <Typography variant="h5" gutterBottom>Template Performance</Typography>
          <Grid container spacing={3}>
            {templatePerformance.map((tp, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <StatCard elevation={2}>
                  <Typography variant="h6" color="text.primary">{tp.template_name}</Typography>
                  <Typography variant="body2">Sent: {tp.sent}</Typography>
                  <Typography variant="body2">Opened: {tp.opened}</Typography>
                  <Typography variant="body2">Clicked: {tp.clicked}</Typography>
                </StatCard>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Box>
  );
}

export default AnalyticsDashboard;
