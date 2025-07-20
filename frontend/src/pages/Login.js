import React, { useState } from "react";
import { loginUser } from "../services/apiService";  //servicio
import { useNavigate, Link } from 'react-router-dom';
import "../css/Login.css";

const Login = ({ setIsAuthenticated, setRole }) => {
  const [formData, setFormData] = useState({ correo: "", password: "" });
  const [error, setError] = useState(""); 
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await loginUser(formData);
      if (result.message === 'Inicio de sesión exitoso.') {  
        navigate('/cita');
        const data = result.usuario;
        setRole(data.rol); 
        setIsAuthenticated(true);
        localStorage.setItem('userId',data._id)
        localStorage.setItem('isAuthenticated', 'true'); 
        localStorage.setItem('rol', data.rol);
      } else {
        alert(result.message);
      } 
      setFormData({correo: "", password: "" });
      setLoading(false);

    } catch (error) {
      console.error("Error al iniciar sesión:", error);
      setError("Credenciales incorrectas o error de servidor");
    }

    setLoading(false);
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>Iniciar Sesión</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="correo">Correo electrónico</label>
            <input
              type="correo"
              id="correo"
              name="correo"
              value={formData.correo}
              onChange={handleChange}
              placeholder="Ingresa tu correo"
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="password">Contraseña</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Ingresa tu contraseña"
              required
            />
          </div>
          <button type="submit" className="login-button" disabled={loading}>
            {loading ? "Cargando..." : "Ingresar"}
          </button>
        </form>
        <p className="register-link">
          ¿No tienes una cuenta? <Link to="/register">Regístrate aquí</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
