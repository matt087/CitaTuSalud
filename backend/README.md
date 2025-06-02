# CitaTuSalud API

API desarrollada con Flask para gestionar usuarios, especialidades médicas, horarios y citas.

## Características

- Registro e inicio de sesión de usuarios  
- Registro de especialidades médicas  
- Registro de horarios para doctores  
- Documentación automática con Swagger

## Tecnologías

- Flask  
- SQLite  
- SQLAlchemy  
- Flask-Bcrypt  
- Flasgger (Swagger UI)

## Instalación

1. Clona este repositorio o descarga los archivos.

2. (Opcional) Crea un entorno virtual y actívalo:

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```
3. Instala las dependencias necesarias ejecutando:
```bash
pip install Flask 
pip install Flask-SQLAlchemy  
pip install Flask-Bcrypt  
pip install Flask-Flasgger 
```
4. También puedes instalar las dependencias utilizando:
```bash
pip install -r requirements.txt
```
## Ejecutar la aplicación
Ejecuta el servidor Flask:
```bash
python app.py
```
Por defecto, la aplicación correrá en http://localhost:5000.

## Acceder a la documentación API
La documentación Swagger estará disponible en el navegador en la siguiente URL:
http://localhost:5000/apidocs/


