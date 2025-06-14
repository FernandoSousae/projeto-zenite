// frontend/src/pages/HomePage.jsx
import { Typography, Paper } from '@mui/material';

function HomePage() {
  return (
    <Paper elevation={3} sx={{ mt: 4, p: 2 }}>
      <Typography variant="h5" component="h2">
        Bem-vindo ao Projeto Zênite!
      </Typography>
      <Typography sx={{ mt: 2 }}>
        Selecione uma opção na barra de navegação para começar.
      </Typography>
    </Paper>
  );
}

export default HomePage;