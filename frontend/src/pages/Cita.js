import React, { useState, useEffect } from 'react';
import '../css/Cita.css';
import { fetchEspecialidades, registrarCita, fetchDoctores, fetchHorariosDisponibles } from '../services/apiService';
import { useNavigate } from "react-router-dom";

const Cita = () => {
  const [especialidades, setEspecialidades] = useState([]);
  const [selectedEspecialidad, setSelectedEspecialidad] = useState('');
  const [date, setDate] = useState("");
  const [doctores, setDoctores] = useState([]);
  const [selectedDoctor, setSelectedDoctor] = useState('');
  const [availableHours, setAvailableHours] = useState([]);
  const [hour, setHour] = useState("");
  const [reason, setReason] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
      const getEspecialidades = async () => {
        const data = await fetchEspecialidades();
        setEspecialidades(data);
      };
      getEspecialidades();
    }, []);
  
    useEffect(() => {
      const getDoctores = async () => {
        if (selectedEspecialidad) {
          const data = await fetchDoctores(selectedEspecialidad);
          setDoctores(data);
        }
      };
      getDoctores();
    }, [selectedEspecialidad]);

    useEffect(() => {
      const getHorarios = async () => {
        if (selectedDoctor && date) {
          const data = await fetchHorariosDisponibles(selectedDoctor, date);
          setAvailableHours(data);
        }
      };
      getHorarios();
    }, [selectedDoctor, date]);
  

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedEspecialidad || !selectedDoctor || !selectedEspecialidad || !date || !hour || !reason) {
      alert('Por favor, completa todos los campos.');
      return;
  }
    const userId = localStorage.getItem('userId');
    const CitaData = { 
      pacienteId: userId,
      doctorId: selectedDoctor,
      especialidad: selectedEspecialidad,
      fecha: date,
      hora: hour,
      motivo: reason,
  }
    const result = await registrarCita(CitaData);
    if (result.message === 'Cita registrada exitosamente.') {
        alert(result.message);
        navigate("/MisCitas"); 
      }else{
      alert("Error al registar la cita");
      }
  };

  return (
    <div className="form-container">
      <div className="form-container-box">
        <h2>Formulario de Cita Médica</h2>
        <form className="appointment-form" onSubmit={handleSubmit}>
          <div className="form-group">
          <div className="form-group">
            <label>Especialidad:</label>
            <select
              className="input-field"
              value={selectedEspecialidad}
              onChange={(e) => setSelectedEspecialidad(e.target.value)}
            >
              <option value="">Seleccione una especialidad</option>
              {especialidades.map((especialidad, index) => (
                <option key={index} value={especialidad.nombre}>
                  {especialidad.nombre}
                </option>
              ))}
            </select>
          </div>
          </div>

          {doctores.length > 0 && (
            <div className="form-group">
              <label>Doctor:</label>
              <select
                className="input-field"
                value={selectedDoctor}
                onChange={(e) => setSelectedDoctor(e.target.value)}
              >
                <option value="">Seleccione un doctor</option>
                {doctores.map((doctor, index) => (
                  <option key={index} value={doctor}>
                    {doctor}
                  </option>
                ))}
              </select>
            </div>
          )}
          <div className="form-group">
            <label>Fecha:</label>
            <input
              type="date"
              className="input-field"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>

          
          {availableHours.length > 0 && (
          <div className="form-group">
          <label>Hora:</label>
          <select
            className="select-input"
            value={hour}
            onChange={(e) => setHour(e.target.value)}
          >
            <option value="">Seleccione una hora</option>
            {availableHours.map((hora, index) => (
              <option key={index} value={hora}>
                {hora}
              </option>
            ))}
          </select>
          </div>
        )}
          

          
          <div className="form-group">
            <label>Motivo de consulta:</label>
            <input
              type="text"
              className="input-field"
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              placeholder="Ingrese el motivo de consulta"
            />
          </div>

          <button className="submit-button" type="submit">Enviar</button>
        </form>
      </div>
    </div>
  );
};

export default Cita;
