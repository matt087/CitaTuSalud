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
        
        user = User.query.filter_by(correo='test@example.com').first()
        assert user is not None
        assert user.nombre == 'Test User'
        assert user.rol == 'paciente'
    
    def test_register_missing_fields(self, client):
        """Test registro con campos faltantes"""
        data = {
            'nombre': 'Test User',
            'correo': 'test@example.com'
            # password faltante
        }
        response = client.post('/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Todos los campos son requeridos'
    
    def test_register_duplicate_email(self, client, sample_user):
        """Test registro con correo duplicado"""
        data = {
            'nombre': 'Another User',
            'correo': 'juan@test.com',  # Email ya existe
            'password': 'password123',
            'rol': 'paciente'
        }
        response = client.post('/register',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['message'] == 'El correo ya está registrado.'
    
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
        assert json_data['usuario']['rol'] == 'paciente'
    
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
    
    def test_login_wrong_password(self, client, sample_user):
        """Test login con contraseña incorrecta"""
        data = {
            'correo': 'juan@test.com',
            'password': 'wrongpassword'
        }
        response = client.post('/login',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 401
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Contraseña incorrecta.'