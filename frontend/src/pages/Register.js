import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { registerUser } from "../services/apiService";
import "../css/Register.css";

const Register = () => {
    const [formData, setFormData] = useState({
      nombre: "",
      correo: "",
      password: "",
    });
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
  
    const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData({ ...formData, [name]: value });
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
  
      if (!formData.nombre || !formData.correo || !formData.password) {
        alert("Por favor, completa todos los campos.")
        setLoading(false);
        return;
      }
  
      try {
        const result = await registerUser({
          nombre: formData.nombre,
          correo: formData.correo,
          password: formData.password,
          rol: 2,  // Siempre Paciente
        });
  
        if (result.message === "Usuario registrado con éxito.") {
          alert(result.message);
          navigate("/login"); 
        } else if (result.message === "El correo ya está registrado."){
          alert(result.message);
          navigate("/register"); 
        }else {
          alert("Error al registrar el usuario")
        }
        setFormData({
          nombre: "",
          correo: "",
          password: "",
        });
      } catch (error) {
        alert("Error al registrar el usuario.")
        console.error("Error al registrar el usuario:", error);
      }
  
      setLoading(false);
    };

  return (
    <div className="register-container">
      <div className="register-box">
        <h2>Registrarse</h2>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="nombre">Nombre</label>
            <input
              type="text"
              id="nombre"
              name="nombre"
              value={formData.nombre}
              onChange={handleChange}
              placeholder="Ingresa tu nombre"
              required
            />
          </div>
          <div className="input-group">
            <label htmlFor="correo">Correo electrónico</label>
            <input
              type="email"
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
          <button type="submit" className="register-button" disabled={loading}>
            {loading ? "Registrando..." : "Registrar"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;
