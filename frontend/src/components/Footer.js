import React from 'react';
import '../css/Footer.css'; 


const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p className="footer-text">© 2025 Consultorios Médicos "Su Salud". Todos los derechos reservados.</p>
        <a href="https://wa.me/+593XXXXXXXXX" className="whatsapp-link" target="_blank" rel="noopener noreferrer">
          <button className="whatsapp-button">Contáctanos por WhatsApp</button>
        </a>
      </div>
    </footer>
  );
};

export default Footer;
