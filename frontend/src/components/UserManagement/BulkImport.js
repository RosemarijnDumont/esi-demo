import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { 
  Box, 
  Button, 
  CircularProgress, 
  Alert, 
  Typography, 
  List,
  ListItem,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

const BulkImport = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [importResult, setImportResult] = useState(null);

  const onDrop = useCallback((acceptedFiles, fileRejections) => {
    if (fileRejections.length > 0) {
      setUploadError('Only CSV files are accepted.');
      setFile(null);
      return;
    }
    setFile(acceptedFiles[0]);
    setUploadError(null);
    setImportResult(null);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.csv']
    },
    multiple: false,
  });

  const handleUpload = async () => {
    if (!file) {
      setUploadError('Please select a CSV file to upload.');
      return;
    }

    setUploading(true);
    setUploadError(null);
    setImportResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/users/bulk-import', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'File upload failed.');
      }

      const result = await response.json();
      setImportResult(result);

    } catch (error) {
      setUploadError(error.message);
    } finally {
      setUploading(false);
      setFile(null); // Clear the file input after attempt
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>Bulk User Import</Typography>
      <Typography variant="body1" gutterBottom>
        Upload a CSV file to bulk import users. The CSV should contain columns like
        