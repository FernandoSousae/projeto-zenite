import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
    TextField, 
    Button, 
    Paper, 
    Typography, 
    Box, 
    FormControl, 
    InputLabel, 
    Select, 
    MenuItem, 
    CircularProgress 
} from '@mui/material';

function RecebimentoCreate() {
    const navigate = useNavigate();
    const { auth } = useAuth();

    const [planoId, setPlanoId] = useState('');
    const [notaFiscalId, setNotaFiscalId] = useState('');
    const [observacoes, setObservacoes] = useState('');
    const [planos, setPlanos] = useState([]);
    const [notasFiscais, setNotasFiscais] = useState([]);
    const [loading, setLoading] = useState(true);

    // VERSÃO CORRIGIDA E SEGURA DO USEEFFECT
    useEffect(() => {
        const fetchDropdownData = async () => {
            try {
                // A configuração com o token de autorização
                const config = {
                    headers: { 'Authorization': `Bearer ${auth.accessToken}` }
                };
                // Busca os dados para os menus de seleção
                const [planosRes, notasRes] = await axios.all([
                    axios.get('http://127.0.0.1:8000/api/planos-compra/', config),
                    axios.get('http://127.0.0.1:8000/api/notas-fiscais/', config)
                ]);
                setPlanos(planosRes.data);
                setNotasFiscais(notasRes.data);
            } catch (error) {
                console.error("Erro ao buscar dados para os formulários", error);
                alert("Não foi possível carregar os dados dos menus. Verifique o console.");
            } finally {
                setLoading(false);
            }
        };

        // AQUI ESTÁ A LÓGICA DE SEGURANÇA:
        // Só executa a busca se tivermos certeza que 'auth' e o token existem.
        if (auth && auth.accessToken) {
            fetchDropdownData();
        } else {
            // Se não houver autenticação, paramos o 'loading' para não ficar uma tela infinita.
            setLoading(false);
        }
    }, [auth]); // A dependência é o objeto 'auth' inteiro.

    const handleSubmit = async (e) => {
        e.preventDefault();
        const novoRecebimento = {
            plano_compra_id: planoId,
            nota_fiscal_id: notaFiscalId,
            observacoes: observacoes,
            itens_a_receber: []
        };
        try {
            await axios.post(
                'http://127.0.0.1:8000/api/recebimentos/',
                novoRecebimento,
                { headers: { 'Authorization': `Bearer ${auth.accessToken}` } }
            );
            alert('Recebimento criado com sucesso!');
            navigate('/recebimentos');
        } catch (err) {
            console.error("Erro ao criar recebimento:", err.response?.data || err);
            alert(`Falha ao criar recebimento. Verifique o console para mais detalhes.`);
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
                        {planos.map((plano) => ( <MenuItem key={plano.id} value={plano.id}>{plano.codigo_plano}</MenuItem> ))}
                    </Select>
                </FormControl>
                <FormControl fullWidth margin="normal" required>
                    <InputLabel id="nota-fiscal-label">Nota Fiscal</InputLabel>
                    <Select labelId="nota-fiscal-label" value={notaFiscalId} label="Nota Fiscal" onChange={(e) => setNotaFiscalId(e.target.value)}>
                        {notasFiscais.map((nf) => ( <MenuItem key={nf.id} value={nf.id}>{nf.numero}</MenuItem> ))}
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