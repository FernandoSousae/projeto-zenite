// frontend/src/components/NavBar.jsx
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom'; // Importante! O Link do React Router

function NavBar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          {/* Este link leva para a página inicial */}
          <Button sx={{color: 'white'}} component={Link} to="/">
            Zênite
          </Button>
        </Typography>

        {/* Este link leva para a lista de planos */}
        <Button color="inherit" component={Link} to="/planos-compra">
          Planos de Compra
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default NavBar;