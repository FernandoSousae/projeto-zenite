// frontend/src/pages/RecebimentoList.jsx

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Typography, Paper, CircularProgress, Alert, List, ListItem, ListItemText, Box, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

function RecebimentoList() {
  const [recebimentos, setRecebimentos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    axios.get('http://127.0.0.1:8000/api/recebimentos/')
      .then(response => {
        setRecebimentos(response.data);
      })
      .catch(err => {
        console.error(err);
        setError('Falha ao carregar os recebimentos.');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <CircularProgress sx={{ display: 'block', margin: 'auto', mt: 8 }}/>;
  if (error) return <Alert severity="error" sx={{ mt: 4 }}>{error}</Alert>;

  return (
    <Paper elevation={3} sx={{ mt: 4, p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h5" component="h2">
          Histórico de Recebimentos
        </Typography>
        <Button
          variant="contained"
          component={RouterLink}
          to="/recebimentos/novo"
        >
          Novo Recebimento
        </Button>
      </Box>

      {recebimentos.length === 0 ? (
        <Typography sx={{ p: 2 }}>Nenhum recebimento encontrado.</Typography>
      ) : (
        <List>
          {recebimentos.map(recebimento => (
            <ListItem key={recebimento.id} divider>
              <ListItemText 
                primary={`Recebimento ID: ${recebimento.id} - Plano: ${recebimento.plano_compra}`}
                secondary={`Data: ${new Date(recebimento.data_recebimento).toLocaleString()}`}
              />
            </ListItem>
          ))}
        </List>
      )}
    </Paper>
  );
}

export default RecebimentoList;