// frontend/src/App.jsx

import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css'; // Vamos manter o CSS por enquanto

function App() {
  // 1. Criamos um "estado" para armazenar a lista de planos que virá da API.
  //    Começa como um array vazio.
  const [planos, setPlanos] = useState([]);

  // 2. Usamos o "useEffect" para executar uma ação quando o componente for montado.
  //    O array vazio `[]` no final garante que isso rode apenas uma vez.
  useEffect(() => {
    // 3. Usamos o Axios para fazer uma requisição GET para nossa API Django.
    axios.get('http://127.0.0.1:8000/api/planos-compra/')
      .then(response => {
        // 4. Se a requisição for bem-sucedida, atualizamos nosso estado com os dados recebidos.
        console.log('Dados recebidos:', response.data); // Ótimo para depuração!
        setPlanos(response.data);
      })
      .catch(error => {
        // 5. Se houver um erro (ex: backend desligado, CORS errado), ele será exibido no console.
        console.error('Ocorreu um erro ao buscar os dados:', error);
      });
  }, []); // O array vazio significa "execute este efeito apenas uma vez".

  // 6. O componente renderiza o HTML.
  return (
    <>
      <h1>Projeto Zênite - Planos de Compra</h1>
      <div className="card">
        <h2>Lista de Planos:</h2>
        <ul>
          {/* 7. Usamos .map() para criar um item de lista para cada plano no nosso estado. */}
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