#!/usr/bin/env python3
"""
Script para configurar la estructura correcta de pruebas
"""

import os
import shutil

def create_directory_structure():
    """Crear la estructura de directorios necesaria"""
    print("📁 Creando estructura de directorios...")
    
    # Crear directorio tests si no existe
    if not os.path.exists('tests'):
        os.makedirs('tests')
        print("✅ Creado directorio tests/")
    else:
        print("ℹ️  Directorio tests/ ya existe")
    
    # Crear __init__.py en tests
    init_file = os.path.join('tests', '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write('# Tests package\n')
        print("✅ Creado tests/__init__.py")

def create_conftest():
    """Crear archivo conftest.py en tests/"""
    conftest_content = '''import pytest
import tempfile
import os
import sys
from datetime import datetime, date

# Agregar el directorio backend al path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

try:
    from api import app, db
    from models import User, Especialidad, Horario, HorarioDetail, Cita
    from flask_bcrypt import Bcrypt
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Backend path: {backend_path}")
    raise

@pytest.fixture
def client():
    """Crea un cliente de prueba para la aplicación Flask"""
    database_fd, database_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()
    
    os.close(database_fd)
    os.unlink(database_path)

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
'''
    
    conftest_path = os.path.join('tests', 'conftest.py')
    with open(conftest_path, 'w', encoding='utf-8') as f:
        f.write(conftest_content)
    print("✅ Creado tests/conftest.py")

def create_test_auth():
    """Crear archivo test_auth.py"""
    test_auth_content = '''import sys
import os
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

import pytest
import json
from models import User

class TestAuth:
    """Pruebas para endpoints de autenticación"""
    
    def test_register_success(self, client):
        """Test registro exitoso de usuario"""
        data = {
            'nombre': 'Test User',
            'correo': 'test@example.com',
            'password': 'password123',
            'rol': 'paciente'
        }
        response = client.post('/register', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Usuario registrado con éxito.'
    
    def test_register_missing_fields(self, client):
        """Test registro con campos faltantes"""
        data = {
            'nombre': 'Test User',
            'correo': 'test@example.com'
        }
        response = client.post('/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Todos los campos son requeridos'
    
    def test_login_success(self, client, sample_user):
        """Test login exitoso"""
        data = {
            'correo': 'juan@test.com',
            'password': 'password123'
        }
        response = client.post('/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Inicio de sesión exitoso.'
        assert json_data['usuario']['nombre'] == 'Juan Perez'
    
    def test_login_user_not_found(self, client):
        """Test login con usuario inexistente"""
        data = {
            'correo': 'noexiste@test.com',
            'password': 'password123'
        }
        response = client.post('/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 404
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Usuario no encontrado.'
'''
    
    test_auth_path = os.path.join('tests', 'test_auth.py')
    with open(test_auth_path, 'w', encoding='utf-8') as f:
        f.write(test_auth_content)
    print("✅ Creado tests/test_auth.py")

def create_test_simple():
    """Crear una prueba simple para verificar que todo funciona"""
    test_simple_content = '''import sys
import os
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

def test_simple_math():
    """Prueba simple para verificar que pytest funciona"""
    assert 2 + 2 == 4

def test_import_app():
    """Prueba para verificar que se puede importar la app"""
    try:
        from api import app
        assert app is not None
        assert app.name == 'api'
    except ImportError as e:
        pytest.fail(f"No se pudo importar la app: {e}")
'''
    
    test_simple_path = os.path.join('tests', 'test_simple.py')
    with open(test_simple_path, 'w', encoding='utf-8') as f:
        f.write(test_simple_content)
    print("✅ Creado tests/test_simple.py")

def create_pytest_ini():
    """Crear archivo pytest.ini"""
    pytest_ini_content = '''[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --strict-markers
    --disable-warnings

markers =
    unit: marca pruebas unitarias
    integration: marca pruebas de integración
    slow: marca pruebas lentas
'''
    
    with open('pytest.ini', 'w', encoding='utf-8') as f:
        f.write(pytest_ini_content)
    print("✅ Creado pytest.ini")

def verify_structure():
    """Verificar que la estructura esté correcta"""
    print("\n🔍 Verificando estructura del proyecto...")
    
    required_items = [
        ('backend/', 'Directorio backend'),
        ('backend/api.py', 'Archivo principal de la API'),
        ('backend/models.py', 'Modelos de base de datos'),
        ('tests/', 'Directorio de pruebas'),
        ('tests/__init__.py', 'Inicializador del paquete tests'),
        ('tests/conftest.py', 'Configuración de pytest'),
        ('tests/test_simple.py', 'Prueba simple'),
        ('tests/test_auth.py', 'Pruebas de autenticación'),
        ('pytest.ini', 'Configuración de pytest')
    ]
    
    all_good = True
    for item, description in required_items:
        if os.path.exists(item):
            print(f"✅ {item} - {description}")
        else:
            print(f"❌ {item} - {description} [FALTANTE]")
            all_good = False
    
    return all_good

def show_next_steps():
    """Mostrar próximos pasos"""
    print("\n" + "=" * 60)
    print("📋 PRÓXIMOS PASOS:")
    print("=" * 60)
    
    print("\n1. Ejecutar prueba simple:")
    print("   python -m pytest tests/test_simple.py -v")
    
    print("\n2. Ejecutar todas las pruebas:")
    print("   python -m pytest tests/ -v")
    
    print("\n3. Ejecutar con cobertura:")
    print("   python -m pytest tests/ --cov=backend.api --cov=backend.models -v")
    
    print("\n4. Si hay errores de import, verificar que:")
    print("   - backend/api.py tenga sintaxis correcta")
    print("   - backend/models.py exista")
    print("   - No haya errores de tipeo en los nombres de archivos")

def main():
    """Función principal"""
    print("🚀 CONFIGURANDO ESTRUCTURA DE PRUEBAS")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('backend'):
        print("❌ No se encuentra el directorio 'backend'")
        print("Asegúrate de ejecutar este script desde el directorio raíz del proyecto")
        return False
    
    # Crear estructura
    create_directory_structure()
    create_pytest_ini()
    create_conftest()
    create_test_simple()
    create_test_auth()
    
    # Verificar estructura
    structure_ok = verify_structure()
    
    if structure_ok:
        print("\n✅ ESTRUCTURA CONFIGURADA CORRECTAMENTE")
        show_next_steps()
        return True
    else:
        print("\n❌ HAY PROBLEMAS CON LA ESTRUCTURA")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        input("\nPresiona Enter para continuar...")
        exit(1)