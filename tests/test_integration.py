import pytest
import json
from models import User, Especialidad, Horario, HorarioDetail, Cita
from datetime import date

@pytest.mark.integration
class TestIntegration:
    """Pruebas de integración completas del sistema"""
    
    def test_flujo_completo_cita(self, client):
        """Test del flujo completo: registro de usuario, especialidad, horario y cita"""
        
        paciente_data = {
            'nombre': 'Ana García',
            'correo': 'ana@test.com',
            'password': 'password123',
            'rol': 'paciente'
        }
        response = client.post('/register',
                             data=json.dumps(paciente_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        doctor_data = {
            'nombre': 'Dr. Martínez',
            'correo': 'doctor@test.com',
            'password': 'doctor123',
            'rol': 'doctor'
        }
        response = client.post('/register',
                             data=json.dumps(doctor_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        especialidad_data = {
            'nombre': 'Pediatría',
            'doctor': 'Dr. Martínez',
            'fechaIngreso': '2024-01-15'
        }
        response = client.post('/register-especialidad',
                             data=json.dumps(especialidad_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        horario_data = {
            'especialidad': 'Pediatría',
            'doctor': 'Dr. Martínez',
            'horario': [
                {
                    'fecha': '2024-12-20',
                    'inicio': '09:00',
                    'fin': '17:00'
                }
            ]
        }
        response = client.post('/register-horario',
                             data=json.dumps(horario_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        response = client.get('/horarios-disponibles?doctorId=Dr. Martínez&fecha=2024-12-20')
        assert response.status_code == 200
        horarios_disponibles = json.loads(response.data)
        assert '09:00' in horarios_disponibles
        
        paciente = User.query.filter_by(correo='ana@test.com').first()
        cita_data = {
            'pacienteId': paciente.id,
            'doctorId': 'Dr. Martínez',
            'especialidad': 'Pediatría',
            'fecha': '2024-12-20',
            'hora': '09:00',
            'motivo': 'Consulta de rutina pediátrica'
        }
        response = client.post('/register-cita',
                             data=json.dumps(cita_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        response = client.get('/horarios-disponibles?doctorId=Dr. Martínez&fecha=2024-12-20')
        assert response.status_code == 200
        horarios_disponibles = json.loads(response.data)
        assert '09:00' not in horarios_disponibles
        
        response = client.get(f'/citas/{paciente.id}')
        assert response.status_code == 200
        citas = json.loads(response.data)
        assert len(citas) == 1
        assert citas[0]['especialidad'] == 'Pediatría'
        assert citas[0]['motivo'] == 'Consulta de rutina pediátrica'
    
    def test_flujo_cancelacion_cita(self, client):
        """Test del flujo de cancelación de citas"""
        
        self._setup_test_data(client)
        
        paciente = User.query.filter_by(correo='test@example.com').first()
        
        cita_data = {
            'pacienteId': paciente.id,
            'doctorId': 'Dr. Test',
            'especialidad': 'Medicina General',
            'fecha': '2024-12-25',
            'hora': '10:00',
            'motivo': 'Chequeo general'
        }
        response = client.post('/register-cita',
                             data=json.dumps(cita_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        response = client.get(f'/citas/{paciente.id}')
        citas = json.loads(response.data)
        cita_id = citas[0]['id']
        
        response = client.delete(f'/citas/{cita_id}')
        assert response.status_code == 200
        
        response = client.get('/horarios-disponibles?doctorId=Dr. Test&fecha=2024-12-25')
        assert response.status_code == 200
        horarios_disponibles = json.loads(response.data)
        assert '10:00' in horarios_disponibles
        
        response = client.get(f'/citas/{paciente.id}')
        citas = json.loads(response.data)
        assert len(citas) == 0
    
    def test_multiples_pacientes_mismo_doctor(self, client):
        """Test de múltiples pacientes agendando con el mismo doctor"""
        
        self._setup_test_data(client)
        
        pacientes_data = [
            {'nombre': 'Paciente 1', 'correo': 'p1@test.com', 'password': 'pass1', 'rol': 'paciente'},
            {'nombre': 'Paciente 2', 'correo': 'p2@test.com', 'password': 'pass2', 'rol': 'paciente'},
            {'nombre': 'Paciente 3', 'correo': 'p3@test.com', 'password': 'pass3', 'rol': 'paciente'}
        ]
        
        pacientes_ids = []
        for paciente_data in pacientes_data:
            response = client.post('/register',
                                 data=json.dumps(paciente_data),
                                 content_type='application/json')
            assert response.status_code == 201
            
            paciente = User.query.filter_by(correo=paciente_data['correo']).first()
            pacientes_ids.append(paciente.id)
        
        horarios = ['09:00', '09:40', '10:20']
        
        for i, (paciente_id, hora) in enumerate(zip(pacientes_ids, horarios)):
            cita_data = {
                'pacienteId': paciente_id,
                'doctorId': 'Dr. Test',
                'especialidad': 'Medicina General',
                'fecha': '2024-12-25',
                'hora': hora,
                'motivo': f'Consulta paciente {i+1}'
            }
            response = client.post('/register-cita',
                                 data=json.dumps(cita_data),
                                 content_type='application/json')
            assert response.status_code == 201
        
        response = client.get('/horarios-disponibles?doctorId=Dr. Test&fecha=2024-12-25')
        assert response.status_code == 200
        horarios_disponibles = json.loads(response.data)
        
        for hora in horarios:
            assert hora not in horarios_disponibles
        
        for paciente_id in pacientes_ids:
            response = client.get(f'/citas/{paciente_id}')
            citas = json.loads(response.data)
            assert len(citas) == 1
    
    def test_login_y_operaciones(self, client):
        """Test de login y operaciones posteriores"""
        
        user_data = {
            'nombre': 'Usuario Login',
            'correo': 'login@test.com',
            'password': 'password123',
            'rol': 'paciente'
        }
        response = client.post('/register',
                             data=json.dumps(user_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        login_data = {
            'correo': 'login@test.com',
            'password': 'password123'
        }
        response = client.post('/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        user_info = json.loads(response.data)
        assert user_info['usuario']['nombre'] == 'Usuario Login'
        assert user_info['usuario']['rol'] == 'paciente'
        
        response = client.get('/get-especialidades')
        assert response.status_code == 404
    
    def _setup_test_data(self, client):
        """Método helper para configurar datos de prueba"""
        # Registrar paciente
        paciente_data = {
            'nombre': 'Test Patient',
            'correo': 'test@example.com',
            'password': 'password123',
            'rol': 'paciente'
        }
        client.post('/register',
                   data=json.dumps(paciente_data),
                   content_type='application/json')
        
        # Registrar especialidad
        especialidad_data = {
            'nombre': 'Medicina General',
            'doctor': 'Dr. Test',
            'fechaIngreso': '2024-01-01'
        }
        client.post('/register-especialidad',
                   data=json.dumps(especialidad_data),
                   content_type='application/json')
        
        # Registrar horario
        horario_data = {
            'especialidad': 'Medicina General',
            'doctor': 'Dr. Test',
            'horario': [
                {
                    'fecha': '2024-12-25',
                    'inicio': '09:00',
                    'fin': '17:00'
                }
            ]
        }
        client.post('/register-horario',
                   data=json.dumps(horario_data),
                   content_type='application/json')