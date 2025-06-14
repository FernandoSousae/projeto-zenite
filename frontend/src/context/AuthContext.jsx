// frontend/src/context/AuthContext.jsx

import { createContext, useState, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('user');
    return storedUser ? JSON.parse(storedUser) : null;
  });
  const token = user?.token;

  axios.defaults.headers.common['Authorization'] = token ? `Token ${token}` : '';

  const login = async (username, password) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/api-token-auth/', {
        username,
        password,
      });
      const userData = {
        token: response.data.token,
        ...response.data.user
      };
      setUser(userData);
      localStorage.setItem('user', JSON.stringify(userData));
      axios.defaults.headers.common['Authorization'] = `Token ${userData.token}`;
      return true;
    } catch (error) {
      console.error("Falha no login", error);
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
    delete axios.defaults.headers.common['Authorization'];
  };

  const value = { user, token, login, logout };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  return useContext(AuthContext);
};