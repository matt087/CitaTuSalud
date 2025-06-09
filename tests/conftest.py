import pytest
import tempfile
import os
import sys
import json
from flask_bcrypt import Bcrypt
from datetime import datetime, date

backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

parent_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_path)

try:
    from api import app, db
    from models import User, Especialidad, Horario, HorarioDetail, Cita
    from flask_bcrypt import Bcrypt
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Backend path: {backend_path}")
    print(f"Current working directory: {os.getcwd()}")
    print("Make sure api.py and models.py are in the backend/ directory")
    print("Current sys.path:")
    for path in sys.path:
        print(f"  - {path}")

    api_file = os.path.join(backend_path, 'api.py')
    models_file = os.path.join(backend_path, 'models.py')
    print(f"¿Existe api.py? {os.path.exists(api_file)} ({api_file})")
    print(f"¿Existe models.py? {os.path.exists(models_file)} ({models_file})")
    raise

@pytest.fixture
def client():
    """Crea un cliente de prueba para la aplicación Flask"""
    database_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE']
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()
    
    os.close(database_fd)
    os.unlink(app.config['DATABASE'])

@pytest.fixture
def bcrypt_instance():
    return Bcrypt(app)

@pytest.fixture
def sample_user(client):
    """Crea un usuario de prueba"""
    bcrypt = Bcrypt(app)
    hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
    user = User(
        nombre='Juan Perez',
        correo='juan@test.com',
        password=hashed_password,
        rol='paciente'
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def sample_doctor(client):
    """Crea un doctor de prueba"""
    bcrypt = Bcrypt(app)
    hashed_password = bcrypt.generate_password_hash('doctor123').decode('utf-8')
    doctor = User(
        nombre='Dr. Smith',
        correo='doctor@test.com',
        password=hashed_password,
        rol='doctor'
    )
    db.session.add(doctor)
    db.session.commit()
    return doctor

@pytest.fixture
def sample_especialidad(client):
    """Crea una especialidad de prueba"""
    especialidad = Especialidad(
        nombre='Cardiología',
        doctor='Dr. Smith',
        fechaIngreso=datetime(2024, 1, 1)
    )
    db.session.add(especialidad)
    db.session.commit()
    return especialidad

@pytest.fixture
def sample_horario(client, sample_especialidad):
    """Crea un horario de prueba"""
    horario = Horario(
        doctorId=sample_especialidad.id,
        doctor='Dr. Smith',
        especialidad='Cardiología'
    )
    db.session.add(horario)
    db.session.commit()
    
    detalle = HorarioDetail(
        fecha=date(2024, 12, 15),
        inicio='09:00',
        fin='17:00',
        horario_id=horario.id
    )
    db.session.add(detalle)
    db.session.commit()
    
    return horario