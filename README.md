CitaTuSalud es una aplicación web diseñada para la gestión de citas médicas, que integra un backend y un frontend robustos, junto con pruebas automatizadas y scripts de utilidad. Este proyecto, desarrollado por Mateo Montenegro, Brenda Simbaña y Juan Donoso, 
tiene como objetivo facilitar el proceso de agendamiento y administración de citas en entornos clínicos.

- Objetivos <br>
a) Implementar un sistema de reserva de citas médicas, optimizando la interacción entre pacientes y profesionales de la salud. <br>  
b) Ofrecer una plataforma escalable y mantenible basada en arquitectura cliente‑servidor.<br>  
c) Garantizar calidad mediante pruebas automatizadas (tests) y scripts de despliegue/distribución (scripts).

- Tecnologías <br>  
Componente	         |   Tecnologías Detalladas <br>  
Backend	             |   Python, frameworks web relacionados (ej. Flask, Django) <br>  
Frontend	           |   JavaScript, HTML, CSS <br>  
Testing	             |   pytest u otra herramienta de testing en Python <br>  
Scripts	             |   Bash o Python para despliegue / migración de datos <br>  
Control de versión	 |   Git / GitHub 

- Estructura del proyecto <br>  
backend/:                 lógica del servidor, rutas, controladores, modelos de datos. <br>  
frontend/:                interfaz de usuario, templates, componentes estáticos. <br>  
scripts/:                 utilidades para automatizar tareas (despliegue, migración, etc.). <br>  
tests/:                   pruebas unitarias y de integración. <br>  
run_tests_final.py:       script principal para ejecución completa de pruebas. <br>  

- Arquitectura <br>  
Cliente‑Servidor:       el frontend se comunica con el backend mediante API REST. <br>  
Modelos de datos:       definidos en Python, representan entidades como usuario, cita, profesional, especialidad, con relaciones claramente establecidas (uno‑a‑muchos, muchos‑a‑muchos). <br>  
  - Separación de capas: <br>  
Capa de presentación:   frontend, páginas y componentes visuales. <br>  
Capa de negocio:        lógica en backend (reservas, cancelaciones, validaciones). <br>  
Capa de datos:          modelo ORM, persistencia en base relacional.
