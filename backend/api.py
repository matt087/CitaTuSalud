from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from models import db, User, Especialidad, Horario, HorarioDetail, Cita
from flasgger import Swagger
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  
bcrypt = Bcrypt(app)

template = {
    "swagger": "2.0",
    "info": {
        "title": "CitaTuSalud",
        "description": "API para gestionar usuarios, especialidades, horarios y citas médicas.",
        "version": "1.0.0",
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    }
}

swagger = Swagger(app, template=template)

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
    """
    Register a new user
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              example: Juan Pérez
              description: Nombre completo del usuario.
            correo:
              type: string
              example: juan@example.com
              description: Correo electrónico del usuario, debe ser único.
            password:
              type: string
              example: password123
              description: Contraseña del usuario.
            rol:
              type: integer
              example: 1
              description: Rol del usuario (1 para paciente, 2 para doctor, etc.).
    responses:
      201:
        description: Usuario registrado con éxito.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Usuario registrado con éxito.
      400:
        description: Solicitud incorrecta, falta de campos requeridos o correo ya registrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Todos los campos son requeridos.
      409:
        description: Conflicto, el correo ya está registrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: El correo ya está registrado.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    password = data.get('password')
    rol = data.get('rol')

    if not nombre or not correo or not password:
        return jsonify({"message": "Todos los campos son requeridos"}), 400

    existing_user = User.query.filter_by(correo=correo).first()
    if existing_user:
        return jsonify({"message": "El correo ya está registrado."}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(nombre=nombre, correo=correo, password=hashed_password, rol=rol)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuario registrado con éxito."}), 201


@app.route('/login', methods=['POST'])
def login():
    """
    Login a user
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            correo:
              type: string
              example: juan@example.com
            password:
              type: string
              example: password123
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            message:
              type: string
              example: Inicio de sesión exitoso.
            usuario:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                nombre:
                  type: string
                  example: Juan Pérez
                rol:
                  type: integer
                  example: 1
      404:
        description: User not found
        schema:
          type: object
          properties:
            message:
              type: string
              example: Usuario no encontrado.
      401:
        description: Invalid password
        schema:
          type: object
          properties:
            message:
              type: string
              example: Contraseña incorrecta.
    """
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
    """
    Register a new specialty
    ---
    tags:
      - Especialidades
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            nombre:
              type: string
              example: Cardiología
              description: Nombre de la especialidad.
            doctor:
              type: string
              example: Dr. Gómez
              description: Nombre del doctor asociado a la especialidad.
            fechaIngreso:
              type: string
              example: 2024-06-01
              description: Fecha de ingreso de la especialidad en formato YYYY-MM-DD.
    responses:
      201:
        description: Especialidad registrada con éxito.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Especialidad registrada con éxito.
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                nombre:
                  type: string
                  example: Cardiología
                doctor:
                  type: string
                  example: Dr. Gómez
                fechaIngreso:
                  type: string
                  example: 2024-06-01
      400:
        description: Solicitud incorrecta, falta de campos requeridos o formato de fecha no válido.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Todos los campos son obligatorios.
    """
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
    """
    Register a new schedule
    ---
    tags:
      - Horarios
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            especialidad:
              type: string
              example: Cardiología
              description: Nombre de la especialidad.
            doctor:
              type: string
              example: Dr. Gómez
              description: Nombre del doctor.
            horario:
              type: array
              items:
                type: object
                properties:
                  fecha:
                    type: string
                    example: 2024-06-10
                    description: Fecha en formato YYYY-MM-DD.
                  inicio:
                    type: string
                    example: "09:00"
                    description: Hora de inicio en formato HH:mm.
                  fin:
                    type: string
                    example: "14:00"
                    description: Hora de fin en formato HH:mm.
    responses:
      201:
        description: Horario registrado con éxito.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Horario registrado con éxito.
      400:
        description: Solicitud incorrecta, especialidad o doctor no encontrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Especialidad o Doctor no encontrado.
    """
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
    """
    Get all specialties
    ---
    tags:
      - Especialidades
    responses:
      200:
        description: Lista de especialidades.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              nombre:
                type: string
                example: Cardiología
              doctor:
                type: string
                example: Dr. Gómez
      404:
        description: No hay especialidades registradas.
        schema:
          type: object
          properties:
            message:
              type: string
              example: No hay especialidades registradas.
    """
    especialidades = Especialidad.query.all()
    if not especialidades:
        return jsonify({"message": "No hay especialidades registradas"}), 404

    datos = [{"id": e.id, "nombre": e.nombre, "doctor": e.doctor} for e in especialidades]
    return jsonify(datos), 200


@app.route('/get-doctores/<string:nombre_especialidad>', methods=['GET'])
def get_doctores(nombre_especialidad):
    """
    Get doctors by specialty
    ---
    tags:
      - Especialidades
    parameters:
      - name: nombre_especialidad
        in: path
        required: true
        type: string
        description: Nombre de la especialidad para buscar doctores.
    responses:
      200:
        description: Lista de doctores para la especialidad.
        schema:
          type: array
          items:
            type: string
            example: Dr. Gómez
      404:
        description: No se encontraron doctores para esta especialidad.
        schema:
          type: object
          properties:
            message:
              type: string
              example: No se encontraron doctores para esta especialidad.
    """
    especialidades = Especialidad.query.filter_by(nombre=nombre_especialidad).all()
    if not especialidades:
        return jsonify({"message": "No se encontraron doctores para esta especialidad"}), 404

    doctores = [e.doctor for e in especialidades]
    return jsonify(doctores), 200


@app.route("/horarios-disponibles", methods=['GET'])
def horarios_disponibles():
    """
    Get available schedules for a doctor on a specific date
    ---
    tags:
      - Horarios
    parameters:
      - name: doctorId
        in: query
        required: true
        type: string
        description: Nombre del doctor.
      - name: fecha
        in: query
        required: true
        type: string
        description: Fecha en formato YYYY-MM-DD.
    responses:
      200:
        description: Lista de horarios disponibles.
        schema:
          type: array
          items:
            type: string
            example: "09:00"
      400:
        description: Doctor o fecha son requeridos.
        schema:
          type: object
          properties:
            error:
              type: string
              example: Doctor y fecha son requeridos.
      404:
        description: No hay horario disponible para esta fecha.
        schema:
          type: object
          properties:
            error:
              type: string
              example: No hay horario disponible para esta fecha.
    """
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
    """
    Register a new appointment
    ---
    tags:
      - Citas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            pacienteId:
              type: integer
              example: 1
              description: ID del paciente.
            doctorId:
              type: string
              example: Dr. Gómez
              description: Nombre del doctor.
            especialidad:
              type: string
              example: Cardiología
              description: Especialidad de la cita.
            fecha:
              type: string
              example: 2024-06-10
              description: Fecha de la cita en formato YYYY-MM-DD.
            hora:
              type: string
              example: "09:00"
              description: Hora de la cita en formato HH:mm.
            motivo:
              type: string
              example: Chequeo general
              description: Motivo de la cita.
    responses:
      201:
        description: Cita registrada exitosamente.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Cita registrada exitosamente.
      400:
        description: Faltan campos requeridos o doctor no encontrado.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Faltan campos requeridos.
    """
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

    return jsonify({"message": "Cita registrada exitosamente."}), 


@app.route('/citas/<int:usuarioId>', methods=['GET'])
def get_citas_usuario(usuarioId):
    """
    Get appointments for a specific user
    ---
    tags:
      - Citas
    parameters:
      - name: usuarioId
        in: path
        required: true
        type: integer
        description: ID del paciente para obtener sus citas.
    responses:
      200:
        description: Lista de citas del paciente.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              pacienteId:
                type: integer
                example: 1
              doctorId:
                type: string
                example: Dr. Gómez
              especialidad:
                type: string
                example: Cardiología
              fecha:
                type: string
                example: 2024-06-10
              hora:
                type: string
                example: "09:00"
              motivo:
                type: string
                example: Chequeo general
      404:
        description: No se encontraron citas para el usuario.
        schema:
          type: object
          properties:
            message:
              type: string
              example: No se encontraron citas para el usuario.
    """
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
    """
    Delete an appointment by ID
    ---
    tags:
      - Citas
    parameters:
      - name: citaId
        in: path
        required: true
        type: integer
        description: ID de la cita a eliminar.
    responses:
      200:
        description: Cita cancelada correctamente.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Cita cancelada correctamente.
      404:
        description: Cita no encontrada.
        schema:
          type: object
          properties:
            message:
              type: string
              example: Cita no encontrada.
    """
    cita = Cita.query.get(citaId)
    if not cita:
        return jsonify({"message": "Cita no encontrada"}), 404
    
    db.session.delete(cita)
    db.session.commit()

    return jsonify({"message": "Cita cancelada correctamente"}), 200



if __name__ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True)