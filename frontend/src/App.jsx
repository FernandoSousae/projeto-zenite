import ProtectedRoute from './components/ProtectedRoute';
// frontend/src/App.jsx
import { CssBaseline } from '@mui/material';
import { Routes, Route } from 'react-router-dom'; // Imports para o roteamento

import NavBar from './components/NavBar'; // Nossa barra de navegação
import HomePage from './pages/HomePage'; // Nossa página inicial
import PlanoCompraList from './pages/PlanoCompraList'; // Nossa lista de planos

import PlanoCompraDetail from './pages/PlanoCompraDetail';
import LoginPage from './pages/LoginPage';
import FornecedorList from './pages/FornecedorList';
import FornecedorCreate from './pages/FornecedorCreate';
import RecebimentoList from './pages/RecebimentoList';
import RecebimentoCreate from './pages/RecebimentoCreate';

function App() {
  return (
    <>
      <CssBaseline />
      <NavBar />
      <main>
        <Routes>
          {/* Rotas Públicas */}
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />

          {/* Rotas Protegidas */}
          <Route 
            path="/planos-compra" 
            element={
              <ProtectedRoute>
                <PlanoCompraList />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/planos-compra/:id" 
            element={
              <ProtectedRoute>
                <PlanoCompraDetail />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/fornecedores" 
            element={
              <ProtectedRoute>
                <FornecedorList />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/fornecedores" 
            element={<ProtectedRoute><FornecedorList /></ProtectedRoute>} 
          />
          {/* Adicione esta nova rota protegida */}
          <Route 
            path="/fornecedores/novo" 
            element={<ProtectedRoute><FornecedorCreate /></ProtectedRoute>} 
          />

          <Route 
            path="/recebimentos" 
            element={<ProtectedRoute><RecebimentoList /></ProtectedRoute>} 
          />

          <Route 
            path="/recebimentos/novo" 
            element={<ProtectedRoute><RecebimentoCreate /></ProtectedRoute>} 
          />
          
        </Routes>
      </main>
    </>
  );
}

export default App;