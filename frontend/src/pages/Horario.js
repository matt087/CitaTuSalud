import React, { useState, useEffect } from 'react';
import { fetchEspecialidades, fetchDoctores, registerHorario } from '../services/apiService';
import '../css/Gestionar.css';

const Gestionar = () => {
  const [especialidades, setEspecialidades] = useState([]);
  const [doctores, setDoctores] = useState([]);
  const [selectedEspecialidad, setSelectedEspecialidad] = useState('');
  const [selectedDoctor, setSelectedDoctor] = useState('');
  const [fecha, setFecha] = useState('');
  const [horaInicio, setHoraInicio] = useState('');
  const [horaFin, setHoraFin] = useState('');

  // Obtener especialidades al cargar el componente
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedEspecialidad || !selectedDoctor || !fecha || !horaInicio || !horaFin) {
        alert('Por favor, completa todos los campos.');
        return;
    }

    const horarioData = {
        doctor: selectedDoctor,
        especialidad: selectedEspecialidad,
        horario: [
            {
              fecha: new Date(fecha).toISOString().split('T')[0],
              inicio: horaInicio,
              fin: horaFin,
            },
        ],
    };

    try {
        const result = await registerHorario(horarioData);
        console.log(result); 
        console.log(horarioData)
        if (result.message === 'Horario registrado con éxito') {
        alert(result.message);
        }else{
        alert("Error al registar horario");
        }
        setSelectedEspecialidad('');
        setSelectedDoctor('');
        setFecha('');
        setHoraInicio('');
        setHoraFin('');

    } catch (error) {
        console.error("Error al registrar el horario", error);
        alert("Ocurrió un error, intente más tarde")
    }
  };

  return (
    <div className="form-container">
      <div className="form-container-box">
        <h2>Registro de Horarios</h2>
        <form className="appointment-form" onSubmit={handleSubmit}>
          
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
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Hora de inicio:</label>
            <input
              type="time"
              className="input-field"
              value={horaInicio}
              onChange={(e) => setHoraInicio(e.target.value)}
            />
          </div>


          <div className="form-group">
            <label>Hora de fin:</label>
            <input
              type="time"
              className="input-field"
              value={horaFin}
              onChange={(e) => setHoraFin(e.target.value)}
            />
          </div>

          <button className="submit-button" type="submit">Enviar</button>
        </form>
      </div>
    </div>
  );
};

export default Gestionar;
