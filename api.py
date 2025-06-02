from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from models import db, User, Especialidad, Horario, HorarioDetail, Cita
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  
bcrypt = Bcrypt(app)

def generar_horarios(inicio, fin):
    horarios = []
    fmt = "%H:%M"
    hora_actual = datetime.strptime(inicio, fmt)
    hora_fin = datetime.strptime(fin, fmt)

    while hora_actual + timedelta(minutes=40) <= hora_fin:
        horarios.append(hora_actual.strftime(fmt))
        hora_actual += timedelta(minutes=40)

    return horarios


# Routes

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    password = data.get('password')
    rol = data.get('rol')

    if not nombre or not correo or not password:
        return jsonify({"message": "Todos los campos son requeridos"}), 400

    existing_user = User.query.filter_by(correo=correo).first()
    if existing_user:
        return jsonify({"message": "El correo ya está registrado."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(nombre=nombre, correo=correo, password=hashed_password, rol=rol)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado con éxito."}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo')
    password = data.get('password')

    user = User.query.filter_by(correo=correo).first()
    if not user:
        return jsonify({"message": "Usuario no encontrado."}), 404

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Contraseña incorrecta."}), 401

    return jsonify({
        "message": "Inicio de sesión exitoso.",
        "usuario": {
            "id": user.id,
            "nombre": user.nombre,
            "rol": user.rol,
        },
    }), 200


@app.route('/register-especialidad', methods=['POST'])
def register_especialidad():
    data = request.get_json()
    nombre = data.get('nombre')
    doctor = data.get('doctor')
    fechaIngreso = data.get('fechaIngreso')

    if not nombre or not doctor or not fechaIngreso:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    existing_especialidad = Especialidad.query.filter_by(doctor=doctor).first()
    if existing_especialidad:
        return jsonify({"message": "El nombre ya está registrado."}), 400

    try:
        fecha_ingreso_dt = datetime.strptime(fechaIngreso, '%Y-%m-%d')
    except:
        return jsonify({"error": "Formato de fecha no válido, use YYYY-MM-DD"}), 400

    nueva_especialidad = Especialidad(nombre=nombre, doctor=doctor, fechaIngreso=fecha_ingreso_dt)
    db.session.add(nueva_especialidad)
    db.session.commit()

    return jsonify({"message": "Especialidad registrada con éxito", "data": {
        "id": nueva_especialidad.id,
        "nombre": nueva_especialidad.nombre,
        "doctor": nueva_especialidad.doctor,
        "fechaIngreso": nueva_especialidad.fechaIngreso.strftime('%Y-%m-%d')
    }}), 201


@app.route('/register-horario', methods=['POST'])
def register_horario():
    data = request.get_json()
    especialidad = data.get('especialidad')
    doctor = data.get('doctor')
    horario = data.get('horario')

    especialidad_data = Especialidad.query.filter_by(nombre=especialidad, doctor=doctor).first()
    if not especialidad_data:
        return jsonify({"message": "Especialidad o Doctor no encontrado"}), 400

    nuevo_horario = Horario(doctorId=especialidad_data.id, doctor=doctor, especialidad=especialidad)
    db.session.add(nuevo_horario)
    db.session.commit()

    for h in horario:
        try:
            fecha_dt = datetime.strptime(h['fecha'], "%Y-%m-%d").date()
        except:
            db.session.rollback()
            return jsonify({"error": "Formato de fecha incorrecto en horario, use YYYY-MM-DD"}), 400

        nuevo_detalle = HorarioDetail(
            fecha=fecha_dt, 
            inicio=h['inicio'], 
            fin=h['fin'], 
            horario_id=nuevo_horario.id
        )
        db.session.add(nuevo_detalle)

    db.session.commit()
    return jsonify({"message": "Horario registrado con éxito"}), 201


@app.route('/get-especialidades', methods=['GET'])
def get_especialidades():
    especialidades = Especialidad.query.all()
    if not especialidades:
        return jsonify({"message": "No hay especialidades registradas"}), 404

    datos = [{"id": e.id, "nombre": e.nombre, "doctor": e.doctor} for e in especialidades]
    return jsonify(datos), 200


@app.route('/get-doctores/<string:nombre_especialidad>', methods=['GET'])
def get_doctores(nombre_especialidad):
    especialidades = Especialidad.query.filter_by(nombre=nombre_especialidad).all()
    if not especialidades:
        return jsonify({"message": "No se encontraron doctores para esta especialidad"}), 404

    doctores = [e.doctor for e in especialidades]
    return jsonify(doctores), 200


@app.route("/horarios-disponibles", methods=['GET'])
def horarios_disponibles():
    doctor_nombre = request.args.get('doctorId')
    fecha_str = request.args.get('fecha')

    if not doctor_nombre or not fecha_str:
        return jsonify({"error": "Doctor y fecha son requeridos"}), 400

    especialidad_data = Especialidad.query.filter_by(doctor=doctor_nombre).first()
    if not especialidad_data:
        return jsonify({"message": "Doctor no encontrado"}), 400

    id_especialidad = especialidad_data.id

    try:
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except:
        return jsonify({"error": "Formato de fecha incorrecto, use YYYY-MM-DD"}), 400

    horario = Horario.query.filter_by(doctorId=id_especialidad).join(Horario.detalles).filter(HorarioDetail.fecha == fecha_dt).first()
    if not horario:
        return jsonify({"error": "No hay horario disponible para esta fecha"}), 404

    horario_dia = next((h for h in horario.detalles if h.fecha == fecha_dt), None)
    if not horario_dia:
        return jsonify({"error": "No hay horario en esa fecha"}), 404

    horarios_disponibles = generar_horarios(horario_dia.inicio, horario_dia.fin)
    citas_ocupadas_query = Cita.query.filter_by(doctorId=id_especialidad, fecha=fecha_dt).all()
    horarios_ocupados = [cita.hora for cita in citas_ocupadas_query]

    horarios_disponibles = [hora for hora in horarios_disponibles if hora not in horarios_ocupados]

    if not horarios_disponibles:
        return jsonify({"message": "No hay horarios disponibles para este doctor en la fecha seleccionada."}), 404

    return jsonify(horarios_disponibles), 200


@app.route('/register-cita', methods=['POST'])
def register_cita():
    data = request.get_json()
    pacienteId = data.get('pacienteId')
    doctor_nombre = data.get('doctorId')
    especialidad = data.get('especialidad')
    fecha_str = data.get('fecha')
    hora = data.get('hora')
    motivo = data.get('motivo')

    if not pacienteId or not doctor_nombre or not especialidad or not fecha_str or not hora or not motivo:
        return jsonify({"message": "Faltan campos requeridos."}), 400

    especialidad_data = Especialidad.query.filter_by(doctor=doctor_nombre).first()
    if not especialidad_data:
        return jsonify({"message": "Doctor no encontrado"}), 400

    id_especialidad = especialidad_data.id

    try:
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d').date()
    except:
        return jsonify({"error": "Formato de fecha incorrecto para la fecha, use YYYY-MM-DD"}), 400

    existing_appointment = Cita.query.filter_by(doctorId=id_especialidad, fecha=fecha_dt, hora=hora).first()
    if existing_appointment:
        return jsonify({"message": "Este horario ya está ocupado."}), 400

    new_cita = Cita(
        pacienteId=pacienteId,
        doctorId=id_especialidad,
        especialidad=especialidad,
        fecha=fecha_dt,
        hora=hora,
        motivo=motivo
    )
    db.session.add(new_cita)
    db.session.commit()

    return jsonify({"message": "Cita registrada exitosamente."}), 201


@app.route('/citas/<int:usuarioId>', methods=['GET'])
def get_citas_usuario(usuarioId):
    citas = Cita.query.filter_by(pacienteId=usuarioId).all()
    resultado = []
    for cita in citas:
        resultado.append({
            "id": cita.id,
            "pacienteId": cita.pacienteId,
            "doctorId": cita.doctorId,
            "especialidad": cita.especialidad,
            "fecha": cita.fecha.strftime('%Y-%m-%d'),
            "hora": cita.hora,
            "motivo": cita.motivo
        })
    return jsonify(resultado), 200


@app.route('/citas/<int:citaId>', methods=['DELETE'])
def eliminar_cita(citaId):
    cita = Cita.query.get(citaId)
    if not cita:
        return jsonify({"message": "Cita no encontrada"}), 404
    
    db.session.delete(cita)
    db.session.commit()

    return jsonify({"message": "Cita cancelada correctamente"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

