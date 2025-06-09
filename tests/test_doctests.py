"""
Pruebas usando Doctest para funciones utilitarias
"""

import doctest
from datetime import datetime, timedelta

def generar_horarios_doctest(inicio, fin):
    """
    Genera horarios disponibles en intervalos de 40 minutos.
    
    Args:
        inicio (str): Hora de inicio en formato HH:MM
        fin (str): Hora de fin en formato HH:MM
    
    Returns:
        list: Lista de horarios en formato HH:MM
    
    Examples:
        >>> generar_horarios_doctest("09:00", "11:00")
        ['09:00', '09:40', '10:20']
        
        >>> generar_horarios_doctest("08:00", "10:30")
        ['08:00', '08:40', '09:20', '10:00']
        
        >>> generar_horarios_doctest("09:00", "09:30")
        []
        
        >>> generar_horarios_doctest("14:00", "15:20")
        ['14:00', '14:40']
        
        >>> generar_horarios_doctest("23:00", "23:39")
        []
        
        >>> generar_horarios_doctest("16:30", "18:10")
        ['16:30', '17:10']
    """
    horarios = []
    fmt = "%H:%M"
    hora_actual = datetime.strptime(inicio, fmt)
    hora_fin = datetime.strptime(fin, fmt)

    while hora_actual + timedelta(minutes=40) <= hora_fin:
        horarios.append(hora_actual.strftime(fmt))
        hora_actual += timedelta(minutes=40)

    return horarios


def validar_email_doctest(email):
    """
    Valida si un email tiene el formato correcto.
    
    Args:
        email (str): Email a validar
    
    Returns:
        bool: True si el email es válido, False en caso contrario
    
    Examples:
        >>> validar_email_doctest("test@example.com")
        True
        
        >>> validar_email_doctest("usuario@dominio.org")
        True
        
        >>> validar_email_doctest("doctor123@hospital.es")
        True
        
        >>> validar_email_doctest("correo_invalido")
        False
        
        >>> validar_email_doctest("@dominio.com")
        False
        
        >>> validar_email_doctest("test@")
        False
        
        >>> validar_email_doctest("")
        False
        
        >>> validar_email_doctest("usuario.con.puntos@dominio.com")
        True
        
        >>> validar_email_doctest("test@dominio")
        False
    """
    import re
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def calcular_duracion_cita_doctest(inicio, fin):
    """
    Calcula la duración de una cita en minutos.
    
    Args:
        inicio (str): Hora de inicio en formato HH:MM
        fin (str): Hora de fin en formato HH:MM
    
    Returns:
        int: Duración en minutos
    
    Examples:
        >>> calcular_duracion_cita_doctest("09:00", "09:40")
        40
        
        >>> calcular_duracion_cita_doctest("14:30", "15:10")
        40
        
        >>> calcular_duracion_cita_doctest("10:00", "11:30")
        90
        
        >>> calcular_duracion_cita_doctest("23:30", "23:59")
        29
        
        >>> calcular_duracion_cita_doctest("08:15", "09:00")
        45
        
        >>> calcular_duracion_cita_doctest("16:00", "18:00")
        120
    """
    fmt = "%H:%M"
    hora_inicio = datetime.strptime(inicio, fmt)
    hora_fin = datetime.strptime(fin, fmt)
    
    diferencia = hora_fin - hora_inicio
    return int(diferencia.total_seconds() / 60)


def validar_formato_fecha_doctest(fecha):
    """
    Valida si una fecha tiene el formato correcto YYYY-MM-DD.
    
    Args:
        fecha (str): Fecha a validar
    
    Returns:
        bool: True si la fecha es válida, False en caso contrario
    
    Examples:
        >>> validar_formato_fecha_doctest("2024-12-15")
        True
        
        >>> validar_formato_fecha_doctest("2024-01-01")
        True
        
        >>> validar_formato_fecha_doctest("2024-02-29")
        True
        
        >>> validar_formato_fecha_doctest("2024-13-01")
        False
        
        >>> validar_formato_fecha_doctest("2024-12-32")
        False
        
        >>> validar_formato_fecha_doctest("24-12-15")
        False
        
        >>> validar_formato_fecha_doctest("15/12/2024")
        False
        
        >>> validar_formato_fecha_doctest("")
        False
        
        >>> validar_formato_fecha_doctest("fecha-invalida")
        False
    """
    try:
        datetime.strptime(fecha, '%Y-%m-%d')
        return True
    except (ValueError, TypeError):
        return False


def obtener_proximos_horarios_doctest(horarios_disponibles, cantidad=3):
    """
    Obtiene los próximos N horarios disponibles de una lista.
    
    Args:
        horarios_disponibles (list): Lista de horarios en formato HH:MM
        cantidad (int): Cantidad de horarios a obtener (default: 3)
    
    Returns:
        list: Lista con los próximos horarios disponibles
    
    Examples:
        >>> obtener_proximos_horarios_doctest(["09:00", "09:40", "10:20", "11:00", "11:40"])
        ['09:00', '09:40', '10:20']
        
        >>> obtener_proximos_horarios_doctest(["14:30", "15:10"], 2)
        ['14:30', '15:10']
        
        >>> obtener_proximos_horarios_doctest(["16:00"], 3)
        ['16:00']
        
        >>> obtener_proximos_horarios_doctest([], 3)
        []
        
        >>> obtener_proximos_horarios_doctest(["08:00", "08:40", "09:20"], 1)
        ['08:00']
    """
    return horarios_disponibles[:cantidad]


def es_horario_laboral_doctest(hora):
    """
    Verifica si una hora está dentro del horario laboral (08:00 - 18:00).
    
    Args:
        hora (str): Hora en formato HH:MM
    
    Returns:
        bool: True si está en horario laboral, False en caso contrario
    
    Examples:
        >>> es_horario_laboral_doctest("09:00")
        True
        
        >>> es_horario_laboral_doctest("12:30")
        True
        
        >>> es_horario_laboral_doctest("17:59")
        True
        
        >>> es_horario_laboral_doctest("18:00")
        False
        
        >>> es_horario_laboral_doctest("07:59")
        False
        
        >>> es_horario_laboral_doctest("19:30")
        False
        
        >>> es_horario_laboral_doctest("08:00")
        True
        
        >>> es_horario_laboral_doctest("08:01")
        True
    """
    try:
        hora_obj = datetime.strptime(hora, '%H:%M').time()
        inicio_laboral = datetime.strptime('08:00', '%H:%M').time()
        fin_laboral = datetime.strptime('18:00', '%H:%M').time()
        
        return inicio_laboral <= hora_obj < fin_laboral
    except ValueError:
        return False


def formatear_nombre_doctor_doctest(nombre):
    """
    Formatea el nombre de un doctor agregando el prefijo "Dr." si no lo tiene.
    
    Args:
        nombre (str): Nombre del doctor
    
    Returns:
        str: Nombre formateado con prefijo "Dr."
    
    Examples:
        >>> formatear_nombre_doctor_doctest("Juan Pérez")
        'Dr. Juan Pérez'
        
        >>> formatear_nombre_doctor_doctest("Dr. María García")
        'Dr. María García'
        
        >>> formatear_nombre_doctor_doctest("Dra. Ana López")
        'Dra. Ana López'
        
        >>> formatear_nombre_doctor_doctest("Pedro Martínez")
        'Dr. Pedro Martínez'
        
        >>> formatear_nombre_doctor_doctest("")
        'Dr. '
        
        >>> formatear_nombre_doctor_doctest("Dr.Carlos Silva")
        'Dr.Carlos Silva'
    """
    if not nombre.startswith(('Dr. ', 'Dra. ')):
        return f'Dr. {nombre}'
    return nombre


def contar_citas_por_especialidad_doctest(citas, especialidad):
    """
    Cuenta el número de citas para una especialidad específica.
    
    Args:
        citas (list): Lista de diccionarios con información de citas
        especialidad (str): Especialidad a contar
    
    Returns:
        int: Número de citas para la especialidad
    
    Examples:
        >>> citas = [
        ...     {'especialidad': 'Cardiología', 'doctor': 'Dr. A'},
        ...     {'especialidad': 'Pediatría', 'doctor': 'Dr. B'},
        ...     {'especialidad': 'Cardiología', 'doctor': 'Dr. C'}
        ... ]
        >>> contar_citas_por_especialidad_doctest(citas, 'Cardiología')
        2
        
        >>> contar_citas_por_especialidad_doctest(citas, 'Pediatría')
        1
        
        >>> contar_citas_por_especialidad_doctest(citas, 'Neurología')
        0
        
        >>> contar_citas_por_especialidad_doctest([], 'Cardiología')
        0
    """
    return sum(1 for cita in citas if cita.get('especialidad') == especialidad)


if __name__ == "__main__":
    print("Ejecutando doctests...")
    doctest.testmod(verbose=True)