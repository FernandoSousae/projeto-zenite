// frontend/src/pages/PlanoCompraDetail.jsx
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom'; // Hook para pegar parâmetros da URL
import axios from 'axios';
import { Typography, Paper, Box, CircularProgress, Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@mui/material';

function PlanoCompraDetail() {
  // O hook useParams nos dá o 'id' da URL (ex: /planos-compra/1)
  const { id } = useParams(); 
  const [plano, setPlano] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    // Usamos o ID da URL para buscar os dados do plano específico
    axios.get(`http://127.0.0.1:8000/api/planos-compra/${id}/`)
      .then(response => {
        setPlano(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Ocorreu um erro ao buscar os detalhes do plano:', error);
        setLoading(false);
      });
  }, [id]); // O efeito roda sempre que o 'id' da URL mudar

  if (loading) {
    return <CircularProgress sx={{ display: 'block', margin: 'auto', mt: 4 }} />;
  }

  if (!plano) {
    return <Typography>Plano de Compra não encontrado.</Typography>;
  }

  return (
    <Paper elevation={3} sx={{ mt: 4, p: 3 }}>
      <Typography variant="h4" gutterBottom>Detalhes do Plano: {plano.codigo_plano}</Typography>
      <Typography variant="h6">Status: {plano.status}</Typography>
      <Typography>Data de Emissão: {new Date(plano.data_emissao).toLocaleDateString()}</Typography>

      <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>Itens do Plano</Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Material</TableCell>
              <TableCell align="right">Qtd. Prevista</TableCell>
              <TableCell>Cor</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {plano.itens.map((item) => (
              <TableRow key={item.id}>
                <TableCell>{item.material_descricao}</TableCell>
                <TableCell align="right">{item.quantidade_prevista}</TableCell>
                <TableCell>{item.cor || 'N/A'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  );
}

export default PlanoCompraDetail;