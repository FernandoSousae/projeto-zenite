// frontend/src/context/AuthContext.jsx

import { createContext, useState, useContext } from 'react';
import axios from 'axios';

// 1. Cria o Contexto
const AuthContext = createContext(null);

// 2. Cria o Provedor do Contexto
// Este componente irá "envolver" nossa aplicação e fornecer o estado de autenticação
export const AuthProvider = ({ children }) => {
  // Tenta pegar o token do localStorage para manter o usuário logado
  const [token, setToken] = useState(localStorage.getItem('authToken'));

  // Configura o Axios para sempre enviar o token no cabeçalho se ele existir
  axios.defaults.headers.common['Authorization'] = token ? `Token ${token}` : '';

  // Função de Login
  const login = async (username, password) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/api-token-auth/', {
        username,
        password,
      });
      const userToken = response.data.token;
      setToken(userToken);
      localStorage.setItem('authToken', userToken); // Guarda o token no navegador
      axios.defaults.headers.common['Authorization'] = `Token ${userToken}`;
      return true; // Sucesso
    } catch (error) {
      console.error("Falha no login", error);
      return false; // Falha
    }
  };

  // Função de Logout
  const logout = () => {
    setToken(null);
    localStorage.removeItem('authToken');
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = {
    token,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// 3. Cria um "hook" customizado para facilitar o uso do nosso contexto
export const useAuth = () => {
  return useContext(AuthContext);
};