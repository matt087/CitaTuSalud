CitaTuSalud es una aplicación web diseñada para la gestión de citas médicas, que integra un backend y un frontend robustos, junto con pruebas automatizadas y scripts de utilidad. Este proyecto, desarrollado por Mateo Montenegro, Brenda Simbaña y Juan Donoso, 
tiene como objetivo facilitar el proceso de agendamiento y administración de citas en entornos clínicos.

- Objetivos <br>
a) Implementar un sistema de reserva de citas médicas, optimizando la interacción entre pacientes y profesionales de la salud. <br>  
b) Ofrecer una plataforma escalable y mantenible basada en arquitectura cliente‑servidor.
c) Garantizar calidad mediante pruebas automatizadas (tests) y scripts de despliegue/distribución (scripts).

- Tecnologías
Componente	         |   Tecnologías Detalladas
Backend	             |   Python, frameworks web relacionados (ej. Flask, Django) 
Frontend	           |   JavaScript, HTML, CSS
Testing	             |   pytest u otra herramienta de testing en Python
Scripts	             |   Bash o Python para despliegue / migración de datos
Control de versión	 |   Git / GitHub 

- Estructura del proyecto
backend/:                 lógica del servidor, rutas, controladores, modelos de datos.
frontend/:                interfaz de usuario, templates, componentes estáticos.
scripts/:                 utilidades para automatizar tareas (despliegue, migración, etc.).
tests/:                   pruebas unitarias y de integración.
run_tests_final.py:       script principal para ejecución completa de pruebas. 

- Arquitectura
Cliente‑Servidor:       el frontend se comunica con el backend mediante API REST.
Modelos de datos:       definidos en Python, representan entidades como usuario, cita, profesional, especialidad, con relaciones claramente establecidas (uno‑a‑muchos, muchos‑a‑muchos).
  - Separación de capas:
Capa de presentación:   frontend, páginas y componentes visuales.
Capa de negocio:        lógica en backend (reservas, cancelaciones, validaciones).
Capa de datos:          modelo ORM, persistencia en base relacional.
