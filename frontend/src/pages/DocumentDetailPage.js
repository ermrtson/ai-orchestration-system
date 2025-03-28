import React, { useState, useEffect } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { 
  Paper, Typography, Box, Grid, Chip, 
  Card, CardContent, CircularProgress, 
  Alert, Divider, Button, List, ListItem, 
  ListItemText
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function DocumentDetailPage() {
  const { id } = useParams();
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDocument();
  }, [id]);

  const fetchDocument = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/document/${id}`);
      setDocument(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching document:', err);
      setError('Error loading document. It may not exist or has been deleted.');
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
    <Box>
      <Button
        component={RouterLink}
        to="/documents"
        startIcon={<ArrowBackIcon />}
        sx={{ mb: 3 }}
      >
        Back to Documents
      </Button>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : document ? (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper sx={{ p: 3 }}>
              <Typography variant="h4" gutterBottom>
                {document.title || 'Untitled Document'}
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                Added: {formatDate(document.created_at)}
              </Typography>
              <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                {document.tags && document.tags.map((tag, index) => (
                  <Chip key={index} label={tag} />
                ))}
              </Box>
            </Paper>
          </Grid>

          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Summary
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <Typography variant="body1" paragraph>
                  {document.summary || 'No summary available'}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Citation Information
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                {document.citation ? (
                  <List dense>
                    {Object.entries(document.citation).map(([key, value]) => (
                      value && (
                        <ListItem key={key} disablePadding sx={{ py: 0.5 }}>
                          <ListItemText
                            primary={<Typography variant="body2" fontWeight="bold">{key.charAt(0).toUpperCase() + key.slice(1)}</Typography>}
                            secondary={value}
                          />
                        </ListItem>
                      )
                    ))}
                  </List>
                ) : (
                  <Typography variant="body2">
                    No citation information available
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      ) : (
        <Alert severity="info">Document not found</Alert>
      )}
    </Box>
  );
}

export default DocumentDetailPage;