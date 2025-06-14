// frontend/src/pages/FornecedorCreate.jsx
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { TextField, Button, Paper, Typography, Box } from '@mui/material';

function FornecedorCreate() {
  const navigate = useNavigate();
  const [razaoSocial, setRazaoSocial] = useState('');
  const [nomeFantasia, setNomeFantasia] = useState('');
  const [cnpj, setCnpj] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Limpa erros antigos

    const novoFornecedor = {
      razao_social: razaoSocial,
      nome_fantasia: nomeFantasia,
      cnpj: cnpj,
    };

    try {
      // Usamos axios.post para enviar os dados para o endpoint de criação
      await axios.post('http://127.0.0.1:8000/api/fornecedores/', novoFornecedor);
      // Se der certo, navega de volta para a lista
      navigate('/fornecedores');
    } catch (err) {
      console.error("Erro ao criar fornecedor:", err.response.data);
      // Guarda a mensagem de erro da API para exibir ao usuário
      setError(err.response.data); 
    }
  };

  return (
    <Paper elevation={3} sx={{ mt: 4, p: 3 }}>
      <Typography variant="h5" component="h2" gutterBottom>
        Cadastrar Novo Fornecedor
      </Typography>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Razão Social"
          value={razaoSocial}
          onChange={(e) => setRazaoSocial(e.target.value)}
          fullWidth
          required
          margin="normal"
        />
        <TextField
          label="Nome Fantasia"
          value={nomeFantasia}
          onChange={(e) => setNomeFantasia(e.target.value)}
          fullWidth
          margin="normal"
        />
        <TextField
          label="CNPJ"
          value={cnpj}
          onChange={(e) => setCnpj(e.target.value)}
          fullWidth
          required
          margin="normal"
        />
        {/* Exibe erros de validação da API, se houver */}
        {error && (
          <Box sx={{ color: 'error.main', mt: 2 }}>
            {Object.entries(error).map(([field, messages]) => (
              <Typography key={field}>
                <strong>{field}:</strong> {messages.join(', ')}
              </Typography>
            ))}
          </Box>
        )}
        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
          <Button onClick={() => navigate('/fornecedores')}>
            Cancelar
          </Button>
          <Button type="submit" variant="contained" sx={{ ml: 2 }}>
            Salvar
          </Button>
        </Box>
      </form>
    </Paper>
  );
}

export default FornecedorCreate;