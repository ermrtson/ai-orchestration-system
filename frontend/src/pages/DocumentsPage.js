import React, { useState, useEffect } from 'react';
import { 
  Paper, Typography, Box, Grid, Card, CardContent, 
  CardActions, Button, Chip, CircularProgress, Alert
} from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function DocumentsPage() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/documents/`);
      setDocuments(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching documents:', err);
      setError('Error loading documents. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  return (
    <Paper sx={{ p: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4">Documents</Typography>
        <Button 
          variant="contained" 
          component={RouterLink} 
          to="/"
        >
          Upload New
        </Button>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : documents.length === 0 ? (
        <Alert severity="info">
          No documents found. Upload a document to get started.
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {documents.map((document) => (
            <Grid item xs={12} sm={6} md={4} key={document.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" gutterBottom component="div" noWrap>
                    {document.title || 'Untitled Document'}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Added: {formatDate(document.created_at)}
                  </Typography>
                  <Box sx={{ my: 1, height: '80px', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    <Typography variant="body2" component="p">
                      {document.summary ? 
                        (document.summary.length > 150 ? 
                          document.summary.substring(0, 150) + '...' : 
                          document.summary) : 
                        'No summary available'}
                    </Typography>
                  </Box>
                  <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {document.tags && document.tags.map((tag, index) => (
                      <Chip key={index} label={tag} size="small" />
                    ))}
                  </Box>
                </CardContent>
                <CardActions>
                  <Button 
                    size="small" 
                    component={RouterLink} 
                    to={`/documents/${document.id}`}
                  >
                    View Details
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Paper>
  );
}

export default DocumentsPage;