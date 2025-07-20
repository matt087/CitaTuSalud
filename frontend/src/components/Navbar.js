import React from "react";
import { Link, useNavigate } from "react-router-dom";
import "../css/Navbar.css";

const Navbar = ({ isAuthenticated, setIsAuthenticated, rol }) => {
  const navigate = useNavigate();
  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    localStorage.removeItem('rol');
    setIsAuthenticated(false); // Actualizar el estado a no autenticado
    navigate('/');
  };

  return (
    <nav className="navbar">
      <ul className="navbar-list">
        <li>
          <Link to="/">Home</Link>
        </li>
        {!isAuthenticated ? (
          <li>
            <Link to="/login">Login</Link>
          </li>
        ) : (
          <>
            {rol === 1 && (
              <>
                <li>
                  <Link to="/gestionar">Gestionar</Link>
                </li>
                <li>
                  <Link to="/horario">Horario</Link>
                </li>
              </>
            )}
            {rol === 2 && (
              <>
                <li>
                  <Link to="/cita">Citas</Link>
                </li>
                <li>
                  <Link to="/MisCitas"> Mis Citas</Link>
                </li>
              </>
            )}
            <li>
              <button onClick={handleLogout}>Cerrar sesión</button>
            </li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
