// frontend/src/App.jsx
import { CssBaseline } from '@mui/material';
import { Routes, Route } from 'react-router-dom'; // Imports para o roteamento

import NavBar from './components/NavBar'; // Nossa barra de navegação
import HomePage from './pages/HomePage'; // Nossa página inicial
import PlanoCompraList from './pages/PlanoCompraList'; // Nossa lista de planos

function App() {
  return (
    <>
      <CssBaseline />
      <NavBar /> {/* A barra de navegação agora aparece em todas as páginas */}
      <main>
        {/* O componente Routes define a área onde o conteúdo da página mudará */}
        <Routes>
          {/* Cada Route mapeia um caminho (URL) para um componente */}
          <Route path="/" element={<HomePage />} />
          <Route path="/planos-compra" element={<PlanoCompraList />} />
        </Routes>
      </main>
    </>
  );
}

export default App;