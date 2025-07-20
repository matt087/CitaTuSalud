from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flasgger import Swagger
from datetime import datetime, timedelta
from flask_cors import CORS
from bson.objectid import ObjectId
from bson.json_util import dumps, loads

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/CitaTuSalud"
app.config['JSON_AS_ASCII'] = False 

CORS(app, supports_credentials=True)
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

template = {
    "swagger": "2.0",
    "info": {
        "title": "CitaTuSalud API (MongoDB)",
        "description": "API para gestionar usuarios, especialidades, horarios y citas médicas con MongoDB.",
        "version": "1.0.0"
    }
}
swagger = Swagger(app, template=template)


def generar_horarios(inicio, fin):
    """Genera una lista de intervalos de 40 minutos entre una hora de inicio y fin."""
    horarios = []
    fmt = "%H:%M"
    hora_actual = datetime.strptime(inicio, fmt)
    hora_fin = datetime.strptime(fin, fmt)

    while hora_actual + timedelta(minutes=40) <= hora_fin:
        horarios.append(hora_actual.strftime(fmt))
        hora_actual += timedelta(minutes=40)
    return horarios

def get_next_sequence_value(sequence_name):
    """Obtiene el siguiente valor de una secuencia (para idUsuario autoincremental)."""
    sequence_document = mongo.db.counters.find_one_and_update(
        {'_id': sequence_name},
        {'$inc': {'sequence_value': 1}},
        upsert=True,
        return_document=True
    )
    if not sequence_document: # Si es la primera vez, el valor será 1
         mongo.db.counters.insert_one({'_id': sequence_name, 'sequence_value': 1})
         return 1
    return sequence_document['sequence_value']


@app.route('/register', methods=['POST'])
def register():
    """Register a new user (MongoDB)"""
    # (El Swagger docstring no se modifica, ya que la interfaz es la misma)
    data = request.get_json()
    nombre = data.get('nombre')
    correo = data.get('correo')
    password = data.get('password')
    rol = data.get('rol')

    if not nombre or not correo or not password:
        return jsonify({"message": "Todos los campos son requeridos"}), 400

    existing_user = mongo.db.users.find_one({'correo': correo})
    if existing_user:
        return jsonify({"message": "El correo ya está registrado."}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    id_usuario = get_next_sequence_value('idUsuario')
    
    mongo.db.users.insert_one({
        'idUsuario': id_usuario,
        'nombre': nombre,
        'correo': correo,
        'password': hashed_password,
        'rol': rol
    })

    return jsonify({"message": "Usuario registrado con éxito."}), 201


@app.route('/login', methods=['POST'])
def login():
    """Login a user (MongoDB)"""
    data = request.get_json()
    correo = data.get('correo')
    password = data.get('password')

    user = mongo.db.users.find_one({'correo': correo})
    if not user:
        return jsonify({"message": "Usuario no encontrado."}), 404

    if not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"message": "Contraseña incorrecta."}), 401

    return jsonify({
        "message": "Inicio de sesión exitoso.",
        "usuario": {
            "_id": str(user['_id']), # MongoDB usa _id
            "idUsuario": user.get('idUsuario'),
            "nombre": user['nombre'],
            "rol": user['rol'],
        },
    }), 200



@app.route('/register-especialidad', methods=['POST'])
def register_especialidad():
    """Register a new specialty (MongoDB)"""
    data = request.get_json()
    nombre = data.get('nombre')
    doctor = data.get('doctor')
    fechaIngreso = data.get('fechaIngreso')

    if not nombre or not doctor or not fechaIngreso:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    existing_especialidad = mongo.db.especialidades.find_one({'doctor': doctor})
    if existing_especialidad:
        return jsonify({"message": "El doctor ya está registrado."}), 409

    try:
        fecha_ingreso_dt = datetime.strptime(fechaIngreso, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Formato de fecha no válido, use YYYY-MM-DD"}), 400

    result = mongo.db.especialidades.insert_one({
        'nombre': nombre,
        'doctor': doctor,
        'fechaIngreso': fecha_ingreso_dt
    })
    
    new_especialidad = mongo.db.especialidades.find_one({'_id': result.inserted_id})
    return loads(dumps({"message": "Especialidad registrada con éxito", "data": new_especialidad})), 201


@app.route('/register-horario', methods=['POST'])
def register_horario():
    data = request.get_json()
    especialidad = data.get('especialidad')
    doctor = data.get('doctor')
    horario = data.get('horario')

    especialidad_data = mongo.db.especialidades.find_one({'nombre': especialidad, 'doctor': doctor})
    if not especialidad_data:
        return jsonify({"message": "Especialidad o Doctor no encontrado"}), 404

    try:
        horario_con_fechas = [
            {
                'fecha': datetime.strptime(h['fecha'], "%Y-%m-%d"),
                'inicio': h['inicio'],
                'fin': h['fin']
            } for h in horario
        ]
    except ValueError:
        return jsonify({"error": "Formato de fecha incorrecto en horario, use YYYY-MM-DD"}), 400

    mongo.db.horarios.insert_one({
        'doctorId': especialidad_data['_id'],
        'doctor': doctor,
        'especialidad': especialidad,
        'horario': horario_con_fechas
    })
    
    return jsonify({"message": "Horario registrado con éxito"}), 201


@app.route('/get-especialidades', methods=['GET'])
def get_especialidades():
    """Get all specialties (MongoDB)"""
    especialidades = list(mongo.db.especialidades.find({}))
    if not especialidades:
        return jsonify({"message": "No hay especialidades registradas"}), 404
    
    for esp in especialidades:
        esp['_id'] = str(esp['_id'])
        esp['fechaIngreso'] = esp['fechaIngreso'].strftime('%Y-%m-%d')
        
    return jsonify(especialidades), 200


@app.route('/get-doctores/<string:nombre_especialidad>', methods=['GET'])
def get_doctores(nombre_especialidad):
    """Get doctors by specialty (MongoDB)"""
    especialidades = mongo.db.especialidades.find({'nombre': nombre_especialidad})
    doctores = [e['doctor'] for e in especialidades]

    if not doctores:
        return jsonify({"message": "No se encontraron doctores para esta especialidad"}), 404

    return jsonify(doctores), 200


@app.route("/horarios-disponibles", methods=['GET'])
def horarios_disponibles():
    """Get available schedules for a doctor on a specific date (MongoDB)"""
    doctor_nombre = request.args.get('doctorId')
    fecha_str = request.args.get('fecha')

    if not doctor_nombre or not fecha_str:
        return jsonify({"error": "Doctor y fecha son requeridos"}), 400

    especialidad_data = mongo.db.especialidades.find_one({'doctor': doctor_nombre})
    if not especialidad_data:
        return jsonify({"message": "Doctor no encontrado"}), 404

    doctor_id = especialidad_data['_id']

    try:
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({"error": "Formato de fecha incorrecto, use YYYY-MM-DD"}), 400
    
    horario = mongo.db.horarios.find_one({'doctorId': doctor_id, 'horario.fecha': fecha_dt})

    if not horario:
        return jsonify({"error": "No hay horario disponible para esta fecha"}), 404

    horario_dia = next((h for h in horario['horario'] if h['fecha'].date() == fecha_dt.date()), None)
    if not horario_dia:
        return jsonify({"error": "No hay horario definido en esa fecha"}), 404
    
    horarios_generados = generar_horarios(horario_dia['inicio'], horario_dia['fin'])
    
    citas_ocupadas_cursor = mongo.db.citas.find({'doctorId': doctor_id, 'fecha': fecha_dt})
    horarios_ocupados = [cita['hora'] for cita in citas_ocupadas_cursor]

    horarios_disponibles = [h for h in horarios_generados if h not in horarios_ocupados]

    if not horarios_disponibles:
        return jsonify({"message": "No hay horarios disponibles para este doctor en la fecha seleccionada."}), 404

    return jsonify(horarios_disponibles), 200


@app.route('/register-cita', methods=['POST'])
def register_cita():
    """Register a new appointment (MongoDB)"""
    data = request.get_json()
    pacienteId = data.get('pacienteId')
    doctor_nombre = data.get('doctorId')
    especialidad = data.get('especialidad')
    fecha_str = data.get('fecha')
    hora = data.get('hora')
    motivo = data.get('motivo')

    if not all([pacienteId, doctor_nombre, especialidad, fecha_str, hora, motivo]):
        return jsonify({"message": "Faltan campos requeridos."}), 400

    especialidad_data = mongo.db.especialidades.find_one({'doctor': doctor_nombre})
    if not especialidad_data:
        return jsonify({"message": "Doctor no encontrado"}), 404

    doctor_id_obj = especialidad_data['_id']

    try:
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d')
        paciente_id_obj = ObjectId(pacienteId)
    except ValueError:
        return jsonify({"error": "Formato de fecha o ID de paciente incorrecto."}), 400
    except:
        return jsonify({"error": "ID de paciente no válido."}), 400

    existing_cita = mongo.db.citas.find_one({
        'doctorId': doctor_id_obj,
        'fecha': fecha_dt,
        'hora': hora
    })
    if existing_cita:
        return jsonify({"message": "Este horario ya está ocupado."}), 409

    mongo.db.citas.insert_one({
        'pacienteId': paciente_id_obj,
        'doctorId': doctor_id_obj,
        'especialidad': especialidad,
        'fecha': fecha_dt,
        'hora': hora,
        'motivo': motivo
    })

    return jsonify({"message": "Cita registrada exitosamente."}), 201


@app.route('/citas/<string:usuarioId>', methods=['GET'])
def get_citas_usuario(usuarioId):
    """Get appointments for a specific user (MongoDB)"""
    try:
        paciente_id_obj = ObjectId(usuarioId)
    except:
        return jsonify({"message": "ID de usuario no válido"}), 400

    citas_cursor = mongo.db.citas.find({'pacienteId': paciente_id_obj})
    
    resultado_json = loads(dumps(list(citas_cursor)))

    if not resultado_json:
        return jsonify({"message": "No se encontraron citas para el usuario."}), 404

    return jsonify(resultado_json), 200


@app.route('/citas/<string:citaId>', methods=['DELETE'])
def eliminar_cita(citaId):
    """Delete an appointment by ID (MongoDB)"""
    try:
        cita_id_obj = ObjectId(citaId)
    except:
        return jsonify({"message": "ID de cita no válido"}), 400
    
    result = mongo.db.citas.delete_one({'_id': cita_id_obj})

    if result.deleted_count == 0:
        return jsonify({"message": "Cita no encontrada"}), 404

    return jsonify({"message": "Cita cancelada correctamente"}), 200


if __name__ == '__main__':
    app.run(debug=True)