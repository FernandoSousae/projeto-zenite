// frontend/src/pages/RecebimentoCreate.jsx
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, Paper, Typography, Box, FormControl, InputLabel, Select, MenuItem, CircularProgress } from '@mui/material';

function RecebimentoCreate() {
  const navigate = useNavigate();

  // Estados para os dados do formulário
  const [planoId, setPlanoId] = useState('');
  const [notaFiscalId, setNotaFiscalId] = useState('');
  const [observacoes, setObservacoes] = useState('');

  // Estados para popular os menus de seleção
  const [planos, setPlanos] = useState([]);
  const [notasFiscais, setNotasFiscais] = useState([]);

  const [loading, setLoading] = useState(true);

  // Busca os dados para os menus de seleção quando o componente carrega
  useEffect(() => {
    const fetchDropdownData = async () => {
      try {
        const [planosRes, notasRes] = await axios.all([
          axios.get('http://127.0.0.1:8000/api/planos-compra/'),
          axios.get('http://127.0.0.1:8000/api/notas-fiscais/')
        ]);
        setPlanos(planosRes.data);
        setNotasFiscais(notasRes.data);
      } catch (error) {
        console.error("Erro ao buscar dados para os formulários", error);
      } finally {
        setLoading(false);
      }
    };
    fetchDropdownData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const novoRecebimento = {
      plano_compra: planoId,
      nota_fiscal: notaFiscalId,
      observacoes: observacoes,
    };

    try {
      await axios.post('http://127.0.0.1:8000/api/recebimentos/', novoRecebimento);
      navigate('/recebimentos');
    } catch (err) {
      console.error("Erro ao criar recebimento:", err.response.data);
    }
  };

  if (loading) return <CircularProgress />;

  return (
    <Paper elevation={3} sx={{ mt: 4, p: 3 }}>
      <Typography variant="h5" gutterBottom>Iniciar Novo Recebimento</Typography>
      <form onSubmit={handleSubmit}>
        <FormControl fullWidth margin="normal" required>
          <InputLabel id="plano-compra-label">Plano de Compra</InputLabel>
          <Select labelId="plano-compra-label" value={planoId} label="Plano de Compra" onChange={(e) => setPlanoId(e.target.value)}>
            {planos.map((plano) => (
              <MenuItem key={plano.id} value={plano.id}>{plano.codigo_plano}</MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth margin="normal" required>
          <InputLabel id="nota-fiscal-label">Nota Fiscal</InputLabel>
          <Select labelId="nota-fiscal-label" value={notaFiscalId} label="Nota Fiscal" onChange={(e) => setNotaFiscalId(e.target.value)}>
            {notasFiscais.map((nf) => (
              <MenuItem key={nf.id} value={nf.id}>{nf.numero}</MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField label="Observações" value={observacoes} onChange={(e) => setObservacoes(e.target.value)} multiline rows={4} fullWidth margin="normal" />

        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
          <Button onClick={() => navigate('/recebimentos')}>Cancelar</Button>
          <Button type="submit" variant="contained" sx={{ ml: 2 }}>Salvar e Iniciar Conferência</Button>
        </Box>
      </form>
    </Paper>
  );
}

export default RecebimentoCreate;