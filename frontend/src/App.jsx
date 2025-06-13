// frontend/src/App.jsx

import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // Guarda a lista de planos de compra
  const [planos, setPlanos] = useState([]);

  // Efeito que roda uma vez quando o componente carrega
  useEffect(() => {
    // Chamada GET para a nossa API Django
    axios.get('http://127.0.0.1:8000/api/planos-compra/')
      .then(response => {
        // Se der certo, atualiza o estado com os dados
        console.log('Dados recebidos com sucesso:', response.data);
        setPlanos(response.data);
      })
      .catch(error => {
        // Se der errado, mostra o erro no console
        console.error('Ocorreu um erro ao buscar os dados:', error);
      });
  }, []);

  // Renderiza o HTML
  return (
    <>
      <h1>Projeto Zênite - Planos de Compra</h1>
      <div className="card">
        <h2>Lista de Planos:</h2>
        <ul>
          {/* Mapeia a lista de planos e cria um <li> para cada um */}
          {planos.map(plano => (
            <li key={plano.id}>
              {plano.codigo_plano} - Status: {plano.status}
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

export default App;