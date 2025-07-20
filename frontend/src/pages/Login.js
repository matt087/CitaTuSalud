import React, { useState } from "react";
import { loginUser } from "../services/apiService";
import { useNavigate, Link } from "react-router-dom";
import "../css/Login.css";

const Login = ({ setIsAuthenticated, setRole }) => {
  const [formData, setFormData] = useState({ correo: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const result = await loginUser(formData);
      if (result.message === "Inicio de sesión exitoso.") {
        setRole(result.usuario.rol);
        setIsAuthenticated(true);
        localStorage.setItem("userId", result.usuario._id);
        localStorage.setItem("isAuthenticated", "true");
        localStorage.setItem("rol", result.usuario.rol);
        navigate("/cita");
      } else {
        setError(result.message);
      }
    } catch {
      setError("Credenciales incorrectas o error de servidor");
    } finally {
      setLoading(false);
      setFormData({ correo: "", password: "" });
    }
  };

  return (
    <div className="login-container">
      <div className="login-box" role="main" aria-label="Formulario de inicio de sesión">
        <h2>Iniciar Sesión</h2>
        {error && <p className="error" role="alert">{error}</p>}
        <form onSubmit={handleSubmit} noValidate>
          <div className="input-group">
            <label htmlFor="correo">Correo electrónico</label>
            <input
              type="email"
              id="correo"
              name="correo"
              value={formData.correo}
              onChange={handleChange}
              placeholder="ejemplo@correo.com"
              required
              autoComplete="username"
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
              placeholder="********"
              required
              autoComplete="current-password"
              minLength={6}
            />
          </div>
          <button type="submit" className="login-button" disabled={loading} aria-busy={loading}>
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
