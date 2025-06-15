import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { 
    Typography, Paper, Box, CircularProgress, Alert, Grid, 
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow, 
    FormControl, Select, MenuItem, InputLabel, TextField, Button 
} from '@mui/material';

function RecebimentoDetail() {
    const { id } = useParams();
    const [recebimento, setRecebimento] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [divergencias, setDivergencias] = useState(null);

    // Estados para o formulário de adição de item
    const [selectedMaterial, setSelectedMaterial] = useState('');
    const [quantidadeContada, setQuantidadeContada] = useState('');

    // Função para buscar/atualizar os dados do recebimento
    const fetchRecebimento = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/recebimentos/${id}/`);
            setRecebimento(response.data);
        } catch (err) {
            console.error(err);
            setError('Falha ao carregar detalhes do recebimento.');
        } finally {
            setLoading(false);
        }
    };
    
    useEffect(() => {
        setLoading(true);
        fetchRecebimento();
    }, [id]);

    const handleAddItem = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`http://127.0.0.1:8000/api/recebimentos/${id}/adicionar_item/`, {
                material_id: selectedMaterial,
                quantidade_contada: quantidadeContada,
            });
            setSelectedMaterial('');
            setQuantidadeContada('');
            fetchRecebimento(); // Re-busca os dados para atualizar a lista de itens
        } catch (err) {
            console.error("Erro ao adicionar item:", err.response?.data || err.message);
        }
    };

    const handleConciliar = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/recebimentos/${id}/conciliar/`);
            setDivergencias(response.data);
        } catch (err) {
            console.error("Erro ao realizar conciliação:", err);
            setError("Ocorreu um erro ao processar a conciliação.");
        }
    };

    if (loading) return <CircularProgress sx={{ display: 'block', margin: 'auto', mt: 8 }} />;
    if (error) return <Alert severity="error" sx={{ mt: 4 }}>{error}</Alert>;
    if (!recebimento) return <Alert severity="info">Recebimento não encontrado.</Alert>;

    return (
        <Box sx={{ mt: 4, mb: 4 }}>
            <Paper elevation={2} sx={{ p: 2, mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h4">
                    Recebimento ID: {recebimento.id}
                </Typography>
                <Button variant="contained" color="primary" onClick={handleConciliar}>
                    Finalizar e Conciliar
                </Button>
            </Paper>

            <Grid container spacing={4}>
                <Grid item xs={12} md={6}>
                    <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
                        <Typography variant="h6" gutterBottom>Esperado (Plano de Compra)</Typography>
                        <Typography>Código: {recebimento.plano_compra.codigo_plano}</Typography>
                        <Typography>Status: {recebimento.plano_compra.status}</Typography>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={6}>
                    <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
                        <Typography variant="h6" gutterBottom>Declarado (Nota Fiscal)</Typography>
                        <Typography>Número NF: {recebimento.nota_fiscal.numero}</Typography>
                        <Typography>Valor Total: R$ {recebimento.nota_fiscal.valor_total}</Typography>
                    </Paper>
                </Grid>
            </Grid>

            <Paper elevation={3} sx={{ mt: 4, p: 3 }}>
                <Typography variant="h6" gutterBottom>Lançar Itens Contados</Typography>
                <Box component="form" onSubmit={handleAddItem} sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                    <FormControl sx={{ minWidth: 250 }} required>
                        <InputLabel>Material</InputLabel>
                        <Select value={selectedMaterial} onChange={(e) => setSelectedMaterial(e.target.value)} label="Material">
                            {recebimento.plano_compra.itens.map(item => (
                                <MenuItem key={item.material} value={item.material}>
                                    {item.material_descricao}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                    <TextField
                        label="Quantidade Contada"
                        type="number"
                        value={quantidadeContada}
                        onChange={(e) => setQuantidadeContada(e.target.value)}
                        required
                    />
                    <Button type="submit" variant="contained">Adicionar Item</Button>
                </Box>
                <Typography variant="subtitle1" gutterBottom>Itens Já Contados</Typography>
                <TableContainer component={Paper}>
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                <TableCell>Material</TableCell>
                                <TableCell align="right">Quantidade Contada</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {recebimento.itens_recebidos.map((item) => (
                                <TableRow key={item.id}>
                                    <TableCell>{item.material_descricao}</TableCell>
                                    <TableCell align="right">{item.quantidade_contada}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>

            {divergencias && (
                <Paper elevation={3} sx={{ mt: 4, p: 3 }}>
                    <Typography variant="h6" gutterBottom>Resultado da Conciliação</Typography>
                    {divergencias.length === 0 ? (
                        <Alert severity="success">Conciliação concluída sem divergências!</Alert>
                    ) : (
                        <TableContainer component={Paper}>
                            <Table size="small">
                                <TableHead>
                                    <TableRow>
                                        <TableCell>Material</TableCell>
                                        <TableCell align="right">Qtd. Plano</TableCell>
                                        <TableCell align="right">Qtd. NF</TableCell>
                                        <TableCell align="right">Qtd. Recebida</TableCell>
                                        <TableCell>Divergências</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {divergencias.map((div, index) => (
                                        <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                            <TableCell component="th" scope="row">{div.material_codigo}</TableCell>
                                            <TableCell align="right">{div.qtd_plano}</TableCell>
                                            <TableCell align="right">{div.qtd_nf}</TableCell>
                                            <TableCell align="right">{div.qtd_recebida}</TableCell>
                                            <TableCell sx={{ color: 'error.main', fontWeight: 'bold' }}>
                                                {div.tipo_divergencia.join(', ')}
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    )}
                </Paper>
            )}
        </Box>
    );
}

export default RecebimentoDetail;