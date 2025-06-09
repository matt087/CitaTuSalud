import pytest
import json
import sys
import os

backend_path = os.path.join(os.path.dirname(os.getcwd()), 'backend')
if not os.path.exists(backend_path):
    backend_path = os.path.join('.', 'backend')

sys.path.insert(0, backend_path)
sys.path.insert(0, '.')

from models import Especialidad


class TestEspecialidades:
    """Pruebas para endpoints de especialidades"""
    
    def test_register_especialidad_success(self, client):
        """Test registro exitoso de especialidad"""
        data = {
            'nombre': 'Cardiología',
            'doctor': 'Dr. García',
            'fechaIngreso': '2024-01-15'
        }
        response = client.post('/register-especialidad',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Especialidad registrada con éxito'
        assert json_data['data']['nombre'] == 'Cardiología'
        assert json_data['data']['doctor'] == 'Dr. García'
        
        # Verificar en base de datos
        especialidad = Especialidad.query.filter_by(doctor='Dr. García').first()
        assert especialidad is not None
        assert especialidad.nombre == 'Cardiología'
    
    def test_register_especialidad_missing_fields(self, client):
        """Test registro de especialidad con campos faltantes"""
        data = {
            'nombre': 'Cardiología',
            'doctor': 'Dr. García'
            # fechaIngreso faltante
        }
        response = client.post('/register-especialidad',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['error'] == 'Todos los campos son obligatorios'
    
    def test_register_especialidad_duplicate_doctor(self, client, sample_especialidad):
        """Test registro de especialidad con doctor duplicado"""
        data = {
            'nombre': 'Neurología',
            'doctor': 'Dr. Smith',  # Doctor ya existe
            'fechaIngreso': '2024-02-15'
        }
        response = client.post('/register-especialidad',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['message'] == 'El nombre ya está registrado.'
    
    def test_register_especialidad_invalid_date(self, client):
        """Test registro de especialidad con fecha inválida"""
        data = {
            'nombre': 'Cardiología',
            'doctor': 'Dr. García',
            'fechaIngreso': 'fecha-invalida'
        }
        response = client.post('/register-especialidad',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['error'] == 'Formato de fecha no válido, use YYYY-MM-DD'
    
    def test_get_especialidades_success(self, client, sample_especialidad):
        """Test obtener lista de especialidades"""
        response = client.get('/get-especialidades')
        
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert len(json_data) == 1
        assert json_data[0]['nombre'] == 'Cardiología'
        assert json_data[0]['doctor'] == 'Dr. Smith'
    
    def test_get_especialidades_empty(self, client):
        """Test obtener especialidades cuando no hay ninguna"""
        response = client.get('/get-especialidades')
        
        assert response.status_code == 404
        json_data = json.loads(response.data)
        assert json_data['message'] == 'No hay especialidades registradas'
    
    def test_get_doctores_by_especialidad_success(self, client, sample_especialidad):
        """Test obtener doctores por especialidad"""
        response = client.get('/get-doctores/Cardiología')
        
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert len(json_data) == 1
        assert json_data[0] == 'Dr. Smith'
    
    def test_get_doctores_by_especialidad_not_found(self, client):
        """Test obtener doctores de especialidad inexistente"""
        response = client.get('/get-doctores/Inexistente')
        
        assert response.status_code == 404
        json_data = json.loads(response.data)
        assert json_data['message'] == 'No se encontraron doctores para esta especialidad'