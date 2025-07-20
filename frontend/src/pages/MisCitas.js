import React, { useState, useEffect } from 'react';
import { fetchCitasUsuario, cancelarCita } from '../services/apiService';
import { useNavigate } from 'react-router-dom';
import "../css/MisCitas.css";

const MisCitas = () => {
  const [citas, setCitas] = useState([]);
  const usuarioId = localStorage.getItem('userId'); 
  const navigate = useNavigate();

  useEffect(() => {
    const obtenerCitas = async () => {
      const data = await fetchCitasUsuario(usuarioId);
      setCitas(data);
    };
    obtenerCitas();
  }, [usuarioId]);

  const handleCancelar = async (citaId) => {
    console.log("citaId en handleCancelar:", citaId);
    try {
      const result = await cancelarCita(citaId);
      if (result.message === "Cita cancelada correctamente") {
        setCitas(citas.filter(cita => cita._id !== citaId));
        alert(result.message)
        navigate('/MisCitas');
      } else {
        alert('Error al cancelar la cita');
      }
    } catch (error) {
      console.error('Error al cancelar la cita:', error);
    }
  };

  return (
    <div className="mis-citas-container">
      <h2>Mis Citas</h2>
      {citas.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Especialidad</th>
              <th>Fecha</th>
              <th>Hora</th>
              <th>Motivo</th>
              <th>Acción</th>
            </tr>
          </thead>
          <tbody>
          {citas.map((cita) => (
            <tr key={cita._id}>
              <td>{cita.especialidad}</td>
              <td>{cita.fecha?.$date ? new Date(cita.fecha.$date).toLocaleDateString() : cita.fecha}</td>
              <td>{cita.hora}</td>
              <td>{cita.motivo}</td>
              <td>
                <button
                  className="boton"
                  onClick={() => {
                    if (window.confirm(`¿Estás seguro de que deseas cancelar la cita de ${cita.especialidad} el ${cita.fecha} a las ${cita.hora}?`)) {
                      handleCancelar(cita._id);
                    }
                  }}
                >
                  Cancelar
                </button>
              </td>
            </tr>
          ))}

          </tbody>
        </table>
      ) : (
        <p>No tienes citas programadas.</p>
      )}
    </div>
  );
};

export default MisCitas;
