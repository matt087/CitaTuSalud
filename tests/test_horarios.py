import pytest
import json
from models import Horario, HorarioDetail
from app import generar_horarios

class TestHorarios:
    """Pruebas para endpoints de horarios"""
    
    def test_generar_horarios_function(self):
        """Test función generar_horarios"""
        horarios = generar_horarios("09:00", "11:00")
        expected = ["09:00", "09:40", "10:20"]
        assert horarios == expected
        
        horarios_largo = generar_horarios("08:00", "10:30")
        expected_largo = ["08:00", "08:40", "09:20", "10:00"]
        assert horarios_largo == expected_largo
    
    def test_generar_horarios_edge_cases(self):
        """Test casos límite de generar_horarios"""
        horarios_corto = generar_horarios("09:00", "09:30")
        assert horarios_corto == []
        
        horarios_exacto = generar_horarios("09:00", "09:40")
        assert horarios_exacto == []
    
    def test_register_horario_success(self, client, sample_especialidad):
        """Test registro exitoso de horario"""
        data = {
            'especialidad': 'Cardiología',
            'doctor': 'Dr. Smith',
            'horario': [
                {
                    'fecha': '2024-12-15',
                    'inicio': '09:00',
                    'fin': '17:00'
                },
                {
                    'fecha': '2024-12-16',
                    'inicio': '10:00',
                    'fin': '16:00'
                }
            ]
        }
        
        response = client.post('/register-horario',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Horario registrado con éxito'
        
        # Verificar en base de datos
        horario = Horario.query.filter_by(doctor='Dr. Smith').first()
        assert horario is not None
        assert len(horario.detalles) == 2
    
    def test_register_horario_especialidad_not_found(self, client):
        """Test registro de horario con especialidad inexistente"""
        data = {
            'especialidad': 'Inexistente',
            'doctor': 'Dr. Inexistente',
            'horario': [
                {
                    'fecha': '2024-12-15',
                    'inicio': '09:00',
                    'fin': '17:00'
                }
            ]
        }
        
        response = client.post('/register-horario',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Especialidad o Doctor no encontrado'
    
    def test_register_horario_invalid_date(self, client, sample_especialidad):
        """Test registro de horario con fecha inválida"""
        data = {
            'especialidad': 'Cardiología',
            'doctor': 'Dr. Smith',
            'horario': [
                {
                    'fecha': 'fecha-invalida',
                    'inicio': '09:00',
                    'fin': '17:00'
                }
            ]
        }
        
        response = client.post('/register-horario',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['error'] == 'Formato de fecha incorrecto en horario, use YYYY-MM-DD'
    
    def test_horarios_disponibles_success(self, client, sample_horario):
        """Test obtener horarios disponibles"""
        response = client.get('/horarios-disponibles?doctorId=Dr. Smith&fecha=2024-12-15')
        
        assert response.status_code == 200
        json_data = json.loads(response.data)
        # Verificar que devuelve una lista de horarios
        assert isinstance(json_data, list)
        assert len(json_data) > 0
        # El primer horario debería ser 09:00
        assert "09:00" in json_data
    
    def test_horarios_disponibles_missing_params(self, client):
        """Test horarios disponibles con parámetros faltantes"""
        response = client.get('/horarios-disponibles?doctorId=Dr. Smith')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['error'] == 'Doctor y fecha son requeridos'
    
    def test_horarios_disponibles_doctor_not_found(self, client):
        """Test horarios disponibles con doctor inexistente"""
        response = client.get('/horarios-disponibles?doctorId=Dr. Inexistente&fecha=2024-12-15')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Doctor no encontrado'
    
    def test_horarios_disponibles_invalid_date(self, client, sample_especialidad):
        """Test horarios disponibles con fecha inválida"""
        response = client.get('/horarios-disponibles?doctorId=Dr. Smith&fecha=fecha-invalida')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['error'] == 'Formato de fecha incorrecto, use YYYY-MM-DD'
    
    def test_horarios_disponibles_no_schedule(self, client, sample_especialidad):
        """Test horarios disponibles para fecha sin horario"""
        response = client.get('/horarios-disponibles?doctorId=Dr. Smith&fecha=2024-12-20')
        
        assert response.status_code == 404
        json_data = json.loads(response.data)
        assert json_data['error'] == 'No hay horario disponible para esta fecha'