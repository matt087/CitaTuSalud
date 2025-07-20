import axios from 'axios';

const API_URL = 'http://localhost:5000';

export const loginUser = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/login`, credentials, { withCredentials: true });
    return response.data;
  } catch (error) {
    if (error.response) {
      return { message: error.response.data.message }; 
    } else {
      return { message: 'Error en el servidor. Intenta nuevamente más tarde.' };
    }
  }
};

export const registerUser = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/register`, credentials, { withCredentials: true });
    return response.data;
  } catch (error) {
    if (error.response) {
      return { message: error.response.data.message };
    } else {
      return { message: 'Error en el servidor. Intenta nuevamente más tarde.' };
    }
  }
};

export const registerEspecialidad = async (especialidad) => {
  try {
    const response = await axios.post(`${API_URL}/register-especialidad`, especialidad, { withCredentials: true });
    return response.data;
  } catch (error) {
    if (error.response) {
      return { message: error.response.data.message };
    } else {
      return { message: 'Error en el servidor. Intenta nuevamente más tarde.' };
    }
  }
};
export const registerHorario = async (horario) => {
  try {
    const response = await axios.post(`${API_URL}/register-horario`, horario, { withCredentials: true });
    return response.data;
  } catch (error) {
    if (error.response) {
      return { message: error.response.data.message };
    } else {
      return { message: 'Error en el servidor. Intenta nuevamente más tarde.' };
    }
  }
};

export const fetchEspecialidades = async () => {
  try {
    const response = await axios.get(`${API_URL}/get-especialidades`, { withCredentials: true });
    return response.data;
  } catch (error) {
    if (error.response) {
      return { message: error.response.data.message };
    } else {
      return { message: 'Error en el servidor. Intenta nuevamente más tarde.' };
    }
  }
};

export const fetchDoctores = async (especialidad) => {
  try {
    const response = await axios.get(`${API_URL}/get-doctores/${especialidad}`, { withCredentials: true });
    return response.data;
  } catch (error) {
    if (error.response) {
      return { message: error.response.data.message };
    } else {
      return { message: 'Error en el servidor. Intenta nuevamente más tarde.' };
    }
  }
};

export const fetchHorariosDisponibles = async (doctorId, date) => {
  try {
    const response = await axios.get(
      `${API_URL}/horarios-disponibles?doctorId=${encodeURIComponent(doctorId)}&fecha=${encodeURIComponent(date)}`,
      { withCredentials: true }
    );
    return response.data;
  } catch (error) {
    console.error("Error al obtener horarios:", error);
    if (error.response) {
      return { message: error.response.data.message };
    } else {
      return { message: "Error en el servidor. Intenta nuevamente más tarde." };
    }
  }
};

export const registrarCita = async (cita) => {
  try {
    const response = await axios.post(`${API_URL}/register-cita`, cita, { withCredentials: true });
    return response.data;
  } catch (error) {
    if (error.response) {
      return { message: error.response.data.message };
    } else {
      return { message: 'Error en el servidor. Intenta nuevamente más tarde.' };
    }
  }
};

export const fetchCitasUsuario = async (usuarioId) => {
  try {
    const response = await fetch(`${API_URL}/citas/${usuarioId}`);
    const text = await response.text();
    const data = JSON.parse(text); 
    return data;
  } catch (error) {
    console.error("Error al obtener las citas:", error);
    return [];
  }
};

export const cancelarCita = async (citaId) => {
  try {
    const response = await fetch(`${API_URL}/citas/${citaId}`, {
      method: 'DELETE',
    });
    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error al cancelar la cita:", error);
    return { message: "Error al cancelar la cita" };
  }
};
