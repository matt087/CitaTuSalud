import React from 'react';
import '../css/Home.css';
import logo from "../assets/su_salud1.png"; 

const Home = () => {
  return (
    <div className="home-page">
      <h1 className='titulo'>Bienvenido a Consultorios Médicos "Su Salud"</h1>
      
      <p>
        En Consultorios Médicos "Su Salud", nos dedicamos a ofrecer atención médica de calidad para toda la familia.
        Nuestro equipo de especialistas está listo para ayudarte con tus necesidades de salud en diversas áreas.
        En este sistema podrás <strong>agendar o cancelar tus citas</strong> con los especialistas que forman parte de nuestro establecimiento.
      </p>
      
      <h2>Servicios Disponibles</h2>
      <div className="columna">
      <div className="lista">
      <ul>
        <li><strong>Consulta General:</strong> Atención integral para adultos y niños.</li>
        <li><strong>Revisión Rutinaria:</strong> Revisión y tratamiento rutinario para preservar la salud.</li>
        <li><strong>Especialidades Médicas:</strong> Ginecología, Medicina General, Odontología y Fisioterapia.</li>
        <li><strong>Urgencias:</strong> Servicio de atención de urgencias las 24 horas.</li>
        
      </ul>
      </div>
      <div className="logo">
        <img src={logo} alt="Logo" className="login-logo" />
      </div>
      </div>
      <h2>¿Por qué elegirnos?</h2>
      <p>
        - Profesionales altamente capacitados. <br />
        - Consultas en horarios flexibles. <br />
        - Instalaciones modernas y equipadas. <br />
        - Atención personalizada para cada paciente.
      </p>

      <h2>Ubicación</h2>
      <p>
        Nos encontramos en el sector de Guamaní, Quito, Ecuador. Visítanos para recibir la mejor atención médica cerca de ti.
      </p>
      <iframe title="Ubicacion" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d498.71966604496293!2d-78.55805627141565!3d-0.31680935826516876!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x91d5a26d3fb25f15%3A0xe9c68196fd0a9f61!2sConsultorios%20M%C3%A9dicos%20%22Su%20Salud%22!5e0!3m2!1ses!2sec!4v1737390689494!5m2!1ses!2sec" 
      width="400" height="250" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      <h2>Contáctanos</h2>
      <p>
        Para más información o para agendar una cita, puedes llamarnos o escribirnos al <strong>(+593)992838937</strong>.
      </p>
    </div>
  );
};

export default Home;
