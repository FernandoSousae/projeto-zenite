// frontend/src/components/NavBar.jsx
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function NavBar() {
  const { user, logout } = useAuth();
  const isAdminOrAnalyst = user?.groups?.includes('Administrador') || user?.groups?.includes('Analista');
  const canViewRecebimentos = user?.groups?.some(r => ['Administrador', 'Analista', 'Revisor', 'Conferente'].includes(r));

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

        {isAdminOrAnalyst && (
          <Button color="inherit" component={Link} to="/fornecedores">
            Fornecedores
          </Button>
        )}

        {canViewRecebimentos && (
            <Button color="inherit" component={Link} to="/recebimentos">
                Recebimentos
            </Button>
        )}

        {user ? (
          <Button color="inherit" onClick={logout}>
            Logout ({user.username})
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