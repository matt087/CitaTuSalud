from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.Integer, nullable=False)

class Especialidad(db.Model):
    __tablename__ = 'especialidad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    doctor = db.Column(db.String(100), unique=True, nullable=False)
    fechaIngreso = db.Column(db.DateTime, default=datetime.utcnow)

class Horario(db.Model):
    __tablename__ = 'horario'
    id = db.Column(db.Integer, primary_key=True)
    doctorId = db.Column(db.Integer, db.ForeignKey('especialidad.id'), nullable=False)
    doctor = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    detalles = db.relationship('HorarioDetail', backref='horario', lazy=True)

class HorarioDetail(db.Model):
    __tablename__ = 'horario_detail'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    inicio = db.Column(db.String(5), nullable=False)  # HH:mm
    fin = db.Column(db.String(5), nullable=False)     # HH:mm
    horario_id = db.Column(db.Integer, db.ForeignKey('horario.id'), nullable=False)

class Cita(db.Model):
    __tablename__ = 'cita'
    id = db.Column(db.Integer, primary_key=True)
    pacienteId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctorId = db.Column(db.Integer, db.ForeignKey('especialidad.id'), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.String(5), nullable=False)  # HH:mm
    motivo = db.Column(db.String(200), nullable=False)
