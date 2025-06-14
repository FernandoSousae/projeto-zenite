// frontend/src/components/NavBar.jsx
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function NavBar() {
  const { token, logout } = useAuth();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          <Button sx={{color: 'white'}} component={Link} to="/">
            Zênite
          </Button>
        </Typography>

        <Button color="inherit" component={Link} to="/planos-compra">
          Planos de Compra
        </Button>

        {/* Lógica condicional: mostra Logout ou Login */}
        {token ? (
          <Button color="inherit" onClick={logout}>
            Logout
          </Button>
        ) : (
          <Button color="inherit" component={Link} to="/login">
            Login
          </Button>
        )}
      </Toolbar>
    </AppBar>
  );
}

export default NavBar;