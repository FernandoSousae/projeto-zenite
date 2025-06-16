import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Typography, Paper, Box, CircularProgress, Alert, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button, Dialog, DialogTitle, DialogContent, DialogActions, FormControl, InputLabel, Select, MenuItem, TextField, Collapse } from '@mui/material';

function InspecaoQualidadeDetail() {
  const { id } = useParams();
  const [inspecao, setInspecao] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Novos estados para o Modal
  const [modalOpen, setModalOpen] = useState(false);
  const [currentItem, setCurrentItem] = useState(null);
  const [defeitos, setDefeitos] = useState([]); // Para popular o dropdown de defeitos
  const [selectedDefeito, setSelectedDefeito] = useState('');
  const [quantidadeDefeituosa, setQuantidadeDefeituosa] = useState('');
  const [openRowId, setOpenRowId] = useState(null);

  const fetchPageData = async () => {
    setLoading(true);
    try {
      // Fazemos as duas chamadas em paralelo
      const [inspecaoRes, defeitosRes] = await axios.all([
        axios.get(`http://127.0.0.1:8000/api/inspecoes-qualidade/${id}/`),
        axios.get('http://127.0.0.1:8000/api/defeitos/')
      ]);
      setInspecao(inspecaoRes.data);
      setDefeitos(defeitosRes.data);
    } catch (err) {
      console.error(err);
      setError('Falha ao carregar dados da página.');
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    fetchPageData();
  }, [id]);

  const handleOpenModal = (item) => {
    setCurrentItem(item);
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
    setCurrentItem(null);
    setSelectedDefeito('');
    setQuantidadeDefeituosa('');
  };

  const handleDefectSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`http://127.0.0.1:8000/api/inspecoes-qualidade/${id}/registrar_defeito/`, {
        item_recebido_id: currentItem.id,
        defeito_id: selectedDefeito,
        quantidade_defeituosa: quantidadeDefeituosa,
      });
      handleCloseModal();
      fetchPageData(); // Re-busca tudo para atualizar a tela
    } catch (err) {
      console.error("Erro ao registrar defeito:", err.response?.data || err.message);
    }
  };


  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!inspecao) return <Alert severity="info">Inspeção não encontrada.</Alert>;

  return (
    <Box sx={{ mt: 4, mb: 4 }}>
      {/* ... Cabeçalho da página ... (sem alterações) */}
      <Paper elevation={2} sx={{ p: 2, mb: 4 }}><Typography variant="h4">Inspeção de Qualidade (ID: {inspecao.id})</Typography></Paper>

      <Paper elevation={3} sx={{ mt: 4, p: 3 }}>
        <Typography variant="h6" gutterBottom>Itens a Inspecionar</Typography>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Material</TableCell>
                <TableCell align="right">Qtd. Recebida</TableCell>
                <TableCell align="center">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {inspecao.recebimento.itens_recebidos.map((item) => (
                // 1. O Fragment agrupa as duas linhas para cada item
                <React.Fragment key={item.id}>
                  {/* 2. A linha principal que agora é clicável */}
                  <TableRow 
                    onClick={() => setOpenRowId(openRowId === item.id ? null : item.id)}
                    sx={{ cursor: 'pointer', '& > *': { borderBottom: 'unset' } }}
                  >
                    <TableCell>{item.material_descricao}</TableCell>
                    <TableCell align="right">{item.quantidade_contada}</TableCell>
                    <TableCell align="center">
                      {/* 3. O botão para adicionar defeito */}
                      <Button 
                        size="small" 
                        variant="outlined" 
                        onClick={(e) => { e.stopPropagation(); handleOpenModal(item); }}
                      >
                        Adicionar Defeito
                      </Button>
                    </TableCell>
                  </TableRow>
                  {/* 4. A linha expansível com os detalhes */}
                  <TableRow>
                    <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={3}>
                      <Collapse in={openRowId === item.id} timeout="auto" unmountOnExit>
                        <Box sx={{ margin: 1, padding: 2, backgroundColor: '#f9f9f9' }}>
                          <Typography variant="h6" gutterBottom component="div">
                            Defeitos Registrados para este Item
                          </Typography>
                          {item.defeitos_encontrados.length > 0 ? (
                            <Table size="small">
                              <TableHead>
                                <TableRow>
                                  <TableCell>Tipo de Defeito</TableCell>
                                  <TableCell align="right">Quantidade</TableCell>
                                </TableRow>
                              </TableHead>
                              <TableBody>
                                {item.defeitos_encontrados.map((defeito) => (
                                  <TableRow key={defeito.id}>
                                    <TableCell>{defeito.defeito_nome}</TableCell>
                                    <TableCell align="right">{defeito.quantidade_defeituosa}</TableCell>
                                  </TableRow>
                                ))}
                              </TableBody>
                            </Table>
                          ) : (
                            <Typography variant="body2" sx={{p:1}}>Nenhum defeito registrado.</Typography>
                          )}
                        </Box>
                      </Collapse>
                    </TableCell>
                  </TableRow>
                </React.Fragment>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Modal Dialog para Adicionar Defeito */}
      <Dialog open={modalOpen} onClose={handleCloseModal}>
        <DialogTitle>Registrar Defeito para: {currentItem?.material_descricao}</DialogTitle>
        <Box component="form" onSubmit={handleDefectSubmit}>
          <DialogContent>
            <FormControl fullWidth margin="normal" required>
              <InputLabel>Tipo de Defeito</InputLabel>
              <Select value={selectedDefeito} onChange={(e) => setSelectedDefeito(e.target.value)} label="Tipo de Defeito">
                {defeitos.map((defeito) => (
                  <MenuItem key={defeito.id} value={defeito.id}>{defeito.nome}</MenuItem>
                ))}
              </Select>
            </FormControl>
            <TextField
              label="Quantidade Defeituosa"
              type="number"
              value={quantidadeDefeituosa}
              onChange={(e) => setQuantidadeDefeituosa(e.target.value)}
              fullWidth
              margin="normal"
              required
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseModal}>Cancelar</Button>
            <Button type="submit" variant="contained">Salvar Defeito</Button>
          </DialogActions>
        </Box>
      </Dialog>
    </Box>
  );
}

export default InspecaoQualidadeDetail;