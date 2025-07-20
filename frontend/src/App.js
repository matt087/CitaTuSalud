import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Cita from "./pages/Cita";
import Banner from './components/Banner';
import MisCitas from "./pages/MisCitas";
import Gestionar from "./pages/Gestionar";
import NotFound from "./pages/NotFound";
import Footer from './components/Footer'; 
import Register from "./pages/Register"; 
import Horario from "./pages/Horario"; 
import ProtectedRoute from './pages/ProtectedRoute';


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    localStorage.getItem('isAuthenticated') === 'true'
  );
  const [rol, setRole] = useState(localStorage.getItem('rol') || '');

  useEffect(() => {
    // Sincronizar el estado con localStorage
    localStorage.setItem('isAuthenticated', isAuthenticated);
  }, [isAuthenticated]);

  return (
    <Router>
      <Banner />
      <Navbar isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} 
      rol={rol} 
      setRole={setRole} />
      <div className="content">
      
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} setRole={setRole}/>} />
          <Route path="/register" element={<Register />} />
          {/* Ruta específica para rol 1 (admin) */}
        <Route
          path="/gestionar"
          element={
            <ProtectedRoute
              isAuthenticated={isAuthenticated}
              requiredRole={1}
              userRole={rol}
            >
              <Gestionar />
            </ProtectedRoute>
          }
        />
        <Route
          path="/horario"
          element={
            <ProtectedRoute
              isAuthenticated={isAuthenticated}
              requiredRole={1}
              userRole={rol}
            >
              <Horario />
            </ProtectedRoute>
          }
        />

        {/* Ruta específica para rol 2 */}
        <Route
          path="/cita"
          element={
            <ProtectedRoute
              isAuthenticated={isAuthenticated}
              requiredRole={2}
              userRole={rol}
            >
              <Cita />
            </ProtectedRoute>
          }
        />
        <Route
          path="/MisCitas"
          element={
            <ProtectedRoute
              isAuthenticated={isAuthenticated}
              requiredRole={2}
              userRole={rol}
            >
              <MisCitas />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
      <Footer />
    </Router>
  );
}

export default App;
