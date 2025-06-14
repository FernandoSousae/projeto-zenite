
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Typography, List, ListItem, ListItemText, Paper, CircularProgress, Alert } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

function PlanoCompraList() {
  const [planos, setPlanos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
      setLoading(true); // Avisa que estamos começando a carregar
      setError(null);   // Limpa erros anteriores

      axios.get('http://127.0.0.1:8000/api/planos-compra/')
        .then(response => {
          setPlanos(response.data);
        })
        .catch(error => {
          console.error('Ocorreu um erro ao buscar os dados:', error);
          setError('Não foi possível carregar os planos de compra. Tente novamente mais tarde.');
        })
        .finally(() => {
          setLoading(false); // Avisa que o carregamento terminou (seja com sucesso ou erro)
        });
    }, []);

// 1. Se estiver carregando, mostre um spinner.
  if (loading) {
    // Importe o CircularProgress do @mui/material no topo do arquivo
    return <CircularProgress sx={{ display: 'block', margin: 'auto', mt: 8 }} />;
  }

  // 2. Se houver um erro, mostre um alerta.
  if (error) {
    // Importe o Alert do @mui/material no topo do arquivo
    return <Alert severity="error" sx={{ mt: 4 }}>{error}</Alert>;
  }

  // 3. Se não estiver carregando e não houver erro, mostre o conteúdo.
  return (
    <Paper elevation={3} sx={{ mt: 4, p: 2 }}> 
      <Typography variant="h5" component="h2" gutterBottom>
        Lista de Planos de Compra
      </Typography>

      {/* 4. Se a lista de planos estiver vazia, mostre uma mensagem. */}
      {planos.length === 0 ? (
        <Typography sx={{ p: 2 }}>Nenhum plano de compra encontrado.</Typography>
      ) : (
        <List>
          {planos.map(plano => (
            <ListItem 
                key={plano.id} 
                divider
                button
                component={RouterLink} // Não se esqueça de importar o Link as RouterLink
                to={`/planos-compra/${plano.id}`}
            >
              <ListItemText 
                primary={`Plano: ${plano.codigo_plano}`} 
                secondary={`Status: ${plano.status}`} 
              />
            </ListItem>
          ))}
        </List>
      )}
    </Paper>
  );
}

export default PlanoCompraList;