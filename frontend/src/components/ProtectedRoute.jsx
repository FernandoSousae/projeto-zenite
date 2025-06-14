// frontend/src/components/ProtectedRoute.jsx

import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

// Este componente "envolve" as páginas que queremos proteger
function ProtectedRoute({ children }) {
  const { token } = useAuth(); // Pega o token do nosso contexto de autenticação
  const location = useLocation(); // Guarda a página que o usuário tentou acessar

  // Se NÃO houver token...
  if (!token) {
    // ...redireciona o usuário para a página de login.
    // O `replace` evita que a página antiga fique no histórico do navegador.
    // O `state` guarda a página original para podermos voltar pra ela depois do login.
    return <Navigate to="/login" replace state={{ from: location }} />;
  }

  // Se houver um token, apenas renderiza o componente filho (a página protegida).
  return children;
}

export default ProtectedRoute;