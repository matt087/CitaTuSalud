import pytest
import json
import sys
import os
from datetime import date

backend_path = os.path.join(os.path.dirname(os.getcwd()), 'backend')
if not os.path.exists(backend_path):
    backend_path = os.path.join('.', 'backend')

sys.path.insert(0, backend_path)
sys.path.insert(0, '.')

import json
from models import User, Cita


class TestCitas:
    """Pruebas para endpoints de citas"""
    
    def test_register_cita_success(self, client, sample_user, sample_horario):
        """Test registro exitoso de cita"""
        data = {
            'pacienteId': sample_user.id,
            'doctorId': 'Dr. Smith',
            'especialidad': 'Cardiología',
            'fecha': '2024-12-15',
            'hora': '09:00',
            'motivo': 'Consulta de rutina'
        }
        
        response = client.post('/register-cita',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 201
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Cita registrada exitosamente.'
        
        # Verificar en base de datos
        cita = Cita.query.filter_by(pacienteId=sample_user.id).first()
        assert cita is not None
        assert cita.especialidad == 'Cardiología'
        assert cita.hora == '09:00'
        assert cita.motivo == 'Consulta de rutina'
    
    def test_register_cita_missing_fields(self, client, sample_user):
        """Test registro de cita con campos faltantes"""
        data = {
            'pacienteId': sample_user.id,
            'doctorId': 'Dr. Smith',
            'especialidad': 'Cardiología',
            'fecha': '2024-12-15',
            # hora y motivo faltantes
        }
        
        response = client.post('/register-cita',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Faltan campos requeridos.'
    
    def test_register_cita_doctor_not_found(self, client, sample_user):
        """Test registro de cita con doctor inexistente"""
        data = {
            'pacienteId': sample_user.id,
            'doctorId': 'Dr. Inexistente',
            'especialidad': 'Cardiología',
            'fecha': '2024-12-15',
            'hora': '09:00',
            'motivo': 'Consulta de rutina'
        }
        
        response = client.post('/register-cita',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Doctor no encontrado'
    
    def test_register_cita_invalid_date(self, client, sample_user, sample_especialidad):
        """Test registro de cita con fecha inválida"""
        data = {
            'pacienteId': sample_user.id,
            'doctorId': 'Dr. Smith',
            'especialidad': 'Cardiología',
            'fecha': 'fecha-invalida',
            'hora': '09:00',
            'motivo': 'Consulta de rutina'
        }
        
        response = client.post('/register-cita',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['error'] == 'Formato de fecha incorrecto para la fecha, use YYYY-MM-DD'
    
    def test_register_cita_time_conflict(self, client, sample_user, sample_horario):
        """Test registro de cita con conflicto de horario"""
        # Primero crear una cita
        cita_existente = Cita(
            pacienteId=sample_user.id,
            doctorId=sample_horario.doctorId,
            especialidad='Cardiología',
            fecha=date(2024, 12, 15),
            hora='09:00',
            motivo='Primera cita'
        )
        from api import db
        db.session.add(cita_existente)
        db.session.commit()
        
        # Intentar crear otra cita en el mismo horario
        data = {
            'pacienteId': sample_user.id,
            'doctorId': 'Dr. Smith',
            'especialidad': 'Cardiología',
            'fecha': '2024-12-15',
            'hora': '09:00',
            'motivo': 'Segunda cita'
        }
        
        response = client.post('/register-cita',
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Este horario ya está ocupado.'
    
    def test_get_citas_usuario_success(self, client, sample_user, sample_horario):
        """Test obtener citas de un usuario"""
        # Crear una cita de prueba
        cita = Cita(
            pacienteId=sample_user.id,
            doctorId=sample_horario.doctorId,
            especialidad='Cardiología',
            fecha=date(2024, 12, 15),
            hora='09:00',
            motivo='Consulta de rutina'
        )
        from api import db
        db.session.add(cita)
        db.session.commit()
        
        response = client.get(f'/citas/{sample_user.id}')
        
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert len(json_data) == 1
        assert json_data[0]['especialidad'] == 'Cardiología'
        assert json_data[0]['hora'] == '09:00'
        assert json_data[0]['motivo'] == 'Consulta de rutina'
        assert json_data[0]['fecha'] == '2024-12-15'
    
    def test_get_citas_usuario_empty(self, client, sample_user):
        """Test obtener citas de usuario sin citas"""
        response = client.get(f'/citas/{sample_user.id}')
        
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data == []
    
    def test_eliminar_cita_success(self, client, sample_user, sample_horario):
        """Test eliminar cita exitosamente"""
        cita = Cita(
            pacienteId=sample_user.id,
            doctorId=sample_horario.doctorId,
            especialidad='Cardiología',
            fecha=date(2024, 12, 15),   
            hora='09:00',
            motivo='Consulta de rutina'
        )
        from api import db
        db.session.add(cita)
        db.session.commit()
        cita_id = cita.id
        
        response = client.delete(f'/citas/{cita_id}')
        
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Cita cancelada correctamente'
        
        # Verificar que la cita fue eliminada
        cita_eliminada = Cita.query.get(cita_id)
        assert cita_eliminada is None
    
    def test_eliminar_cita_not_found(self, client):
        """Test eliminar cita inexistente"""
        response = client.delete('/citas/999')
        
        assert response.status_code == 404
        json_data = json.loads(response.data)
        assert json_data['message'] == 'Cita no encontrada'