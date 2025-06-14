
import { useState, useEffect } from 'react';
import axios from 'axios';
import { Typography, List, ListItem, ListItemText, Paper, CircularProgress, Alert, Box, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

function FornecedorList() {
  // 1. Nossos três estados: dados, carregamento e erro
  const [fornecedores, setFornecedores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // 2. Lógica de busca de dados atualizada
    setLoading(true);
    setError(null);

    // Mudamos apenas a URL para o endpoint de fornecedores
    axios.get('http://127.0.0.1:8000/api/fornecedores/')
      .then(response => {
        setFornecedores(response.data);
      })
      .catch(error => {
        console.error('Ocorreu um erro ao buscar os fornecedores:', error);
        // Mensagem de erro customizada
        setError('Não foi possível carregar os fornecedores. Tente novamente mais tarde.');
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  // 3. Renderização condicional para loading e erro
  if (loading) {
    return <CircularProgress sx={{ display: 'block', margin: 'auto', mt: 8 }} />;
  }

  if (error) {
    return <Alert severity="error" sx={{ mt: 4 }}>{error}</Alert>;
  }

  // 4. Renderização principal com tratamento de lista vazia
  return (
    <Paper elevation={3} sx={{ mt: 4, p: 2 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h5" component="h2">
          Lista de Fornecedores
        </Typography>
        <Button
          variant="contained"
          component={RouterLink}
          to="/fornecedores/novo"
        >
          Novo Fornecedor
        </Button>
      </Box>

      {fornecedores.length === 0 ? (
        // Mensagem customizada para lista vazia
        <Typography sx={{ p: 2 }}>Nenhum fornecedor encontrado.</Typography>
      ) : (
        <List>
          {fornecedores.map(fornecedor => (
            <ListItem key={fornecedor.id} divider>
              <ListItemText 
                primary={fornecedor.nome_fantasia || fornecedor.razao_social}
                secondary={`CNPJ: ${fornecedor.cnpj}`}
              />
            </ListItem>
          ))}
        </List>
      )}
    </Paper>
  );
}

export default FornecedorList;