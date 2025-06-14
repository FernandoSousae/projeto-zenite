// frontend/src/pages/PlanoCompraList.jsx

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Typography, List, ListItem, ListItemText, Paper } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

function PlanoCompraList() {
  // Toda a lógica de estado e busca de dados agora vive aqui.
  const [planos, setPlanos] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/planos-compra/')
      .then(response => {
        setPlanos(response.data);
      })
      .catch(error => {
        console.error('Ocorreu um erro ao buscar os dados:', error);
      });
  }, []);

  // A lógica de renderização da lista também vive aqui.
  return (
    // Usamos o componente Paper do MUI para criar um "cartão" de fundo
    <Paper elevation={3} sx={{ mt: 4, p: 2 }}> 
      <Typography variant="h5" component="h2" gutterBottom>
        Lista de Planos de Compra
      </Typography>
      <List>
        {planos.map(plano => (
        <ListItem 
            key={plano.id} 
               divider
               button // Faz o item parecer clicável
               component={RouterLink} // Diz ao MUI para se comportar como um Link do Router
               to={`/planos-compra/${plano.id}`} // O destino do link
            >
               <ListItemText 
                   primary={`Plano: ${plano.codigo_plano}`} 
                   secondary={`Status: ${plano.status}`} 
               />
        </ListItem>
        ))}
      </List>
    </Paper>
  );
}

export default PlanoCompraList;