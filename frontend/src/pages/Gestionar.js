import React, { useState } from 'react';
import '../css/Gestionar.css';
import { registerEspecialidad } from "../services/apiService";

const Gestionar = () => {
  const [specialty, setSpecialty] = useState('');
  const [date, setDate] = useState('');
  const [name, setName] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validar que todos los campos estén llenos
    if (!specialty || !name || !date) {
      alert('Por favor, completa todos los campos.');
      return;
    }

    const especialidadData = {
      nombre: specialty,
      doctor: name,
      fechaIngreso: date,
    };

    try {
      const result = await registerEspecialidad(especialidadData);
      if (result.message === 'Especialidad registrada con éxito') {
        alert(result.message);

      }else if (result.message === 'Error al registrar la especialidad'){
        alert(result.message);
      }else if (result.message === "El nombre ya está registrado."){
        alert(result.message);
      }else{
        alert(result.message);
      }
      setSpecialty('');
      setDate('');
      setName('');
      
    } catch (error) {
      alert("Error al registrar la especialidad")
      console.error("Error al registrar la especialidad", error);
    }
  };

  return (
    <div className="form-container">
      <div className="form-container-box">
        <h2>Registro de especialistas</h2>
        <form className="appointment-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <br></br>
            <label>Especialidad:</label>
            <div className="radio-group">
              <label>
                <input
                  type="radio"
                  value="Ginecología"
                  checked={specialty === 'Ginecología'}
                  onChange={(e) => setSpecialty(e.target.value)}
                />
                Ginecología
              </label>
              <label>
                <input
                  type="radio"
                  value="Medicina General"
                  checked={specialty === 'Medicina General'}
                  onChange={(e) => setSpecialty(e.target.value)}
                />
                Medicina General
              </label>
              <label>
                <input
                  type="radio"
                  value="Odontología"
                  checked={specialty === 'Odontología'}
                  onChange={(e) => setSpecialty(e.target.value)}
                />
                Odontología
              </label>
              <label>
                <input
                  type="radio"
                  value="Fisioterapia"
                  checked={specialty === 'Fisioterapia'}
                  onChange={(e) => setSpecialty(e.target.value)}
                />
                Fisioterapia
              </label>
            </div>
          </div>

          <div className="form-group">
            <label>Nombre:</label>
            <input
              type="text"
              className="input-field"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Ingrese el nombre del doctor/a"
            />
          </div>

          <div className="form-group">
            <label>Fecha de ingreso:</label>
            <input
              type="date"
              className="input-field"
              value={date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>

          <button className="submit-button" type="submit">Enviar</button>
        </form>
      </div>
    </div>
  );
};

export default Gestionar;
