#!/usr/bin/env python3
"""
Script para ejecutar todas las pruebas y generar reportes de cobertura
"""

import subprocess
import sys
import os
import doctest
from test_doctests import generar_horarios_doctest, calcular_duracion_cita_doctest

def run_doctests():
    """Ejecuta las pruebas de doctest"""
    print("=" * 60)
    print("EJECUTANDO DOCTESTS")
    print("=" * 60)
    
    import test_doctests
    
    result = doctest.testmod(test_doctests, verbose=True)
    
    print(f"\nDoctests ejecutados: {result.attempted}")
    print(f"Doctests fallidos: {result.failed}")
    print(f"Tasa de éxito: {((result.attempted - result.failed) / result.attempted * 100):.1f}%")
    
    return result.failed == 0

def run_unittests():
    """Ejecuta las pruebas unitarias con pytest"""
    print("\n" + "=" * 60)
    print("EJECUTANDO PRUEBAS UNITARIAS CON PYTEST")
    print("=" * 60)
    
    cmd = [
        sys.executable, '-m', 'pytest',
        '-v',
        '--tb=short',
        '--cov=app',
        '--cov=models',
        '--cov-report=html:htmlcov',
        '--cov-report=term-missing',
        '--cov-report=xml:coverage.xml',
        '--cov-fail-under=60',
        'tests/'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd='.')
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except FileNotFoundError:
        print("Error: pytest no encontrado. Instálelo con: pip install pytest pytest-cov")
        return False

def run_coverage_analysis():
    """Ejecuta análisis de cobertura específico"""
    print("\n" + "=" * 60)
    print("ANÁLISIS DETALLADO DE COBERTURA")
    print("=" * 60)
    
    cmd = [sys.executable, '-m', 'coverage', 'report', '--show-missing']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        cmd_html = [sys.executable, '-m', 'coverage', 'html']
        subprocess.run(cmd_html, capture_output=True)
        
        print("\nReporte HTML generado en: htmlcov/index.html")
        
        return True
    except FileNotFoundError:
        print("Error: coverage no encontrado. Instálelo con: pip install coverage")
        return False

def check_coverage_threshold():
    """Verifica que la cobertura cumpla con el umbral mínimo"""
    print("\n" + "=" * 60)
    print("VERIFICACIÓN DE UMBRAL DE COBERTURA (60%)")
    print("=" * 60)
    
    try:
        cmd = [sys.executable, '-m', 'coverage', 'json']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            import json
            with open('coverage.json', 'r') as f:
                coverage_data = json.load(f)
            
            total_coverage = coverage_data['totals']['percent_covered']
            print(f"Cobertura total: {total_coverage:.2f}%")
            
            if total_coverage >= 60:
                print("✅ Cobertura cumple con el umbral mínimo del 60%")
                return True
            else:
                print("❌ Cobertura NO cumple con el umbral mínimo del 60%")
                return False
        else:
            print("No se pudo obtener datos de cobertura")
            return False
    except Exception as e:
        print(f"Error al verificar cobertura: {e}")
        return False

def generate_test_summary():
    """Genera un resumen de todas las pruebas"""
    print("\n" + "=" * 60)
    print("RESUMEN DE HERRAMIENTAS DE TESTING UTILIZADAS")
    print("=" * 60)
    
    summary = """
    ✅ DOCTEST: Pruebas embebidas en docstrings de funciones
       - Funciones testadas: generar_horarios_doctest, calcular_duracion_cita_doctest
       - Ventajas: Documentación y pruebas en un solo lugar
    
    ✅ UNITTEST: Framework de pruebas unitarias de Python (via pytest)
       - Archivos: test_auth.py, test_especialidades.py, test_horarios.py, test_citas.py
       - Cobertura: Endpoints de autenticación, especialidades, horarios y citas
    
    ✅ PYTEST: Framework moderno de testing
       - Fixtures para configuración de datos de prueba
       - Parametrización de pruebas
       - Marcadores para categorizar pruebas
    
    ✅ COVERAGE.PY: Análisis de cobertura de código
       - Reporte en terminal y HTML
       - Umbral mínimo: 60%
       - Identificación de líneas no cubiertas
    
    ✅ PRUEBAS DE INTEGRACIÓN: Flujos completos del sistema
       - Registro → Especialidad → Horario → Cita
       - Cancelación de citas
       - Múltiples usuarios
    
    ✅ CONFIGURACIÓN COMPLETA:
       - pytest.ini: Configuración de pytest
       - conftest.py: Fixtures compartidos
       - requirements.txt: Dependencias de testing
    """
    
    print(summary)

def main():
    """Función principal para ejecutar todas las pruebas"""
    print("SISTEMA DE PRUEBAS PARA APLICACIÓN DE CITAS MÉDICAS")
    print("=" * 60)
    
    all_passed = True
    
    # Ejecutar doctests
    doctest_result = run_doctests()
    all_passed = all_passed and doctest_result
    
    # Ejecutar pruebas unitarias
    unittest_result = run_unittests()
    all_passed = all_passed and unittest_result
    
    # Análisis de cobertura
    coverage_result = run_coverage_analysis()
    all_passed = all_passed and coverage_result
    
    # Verificar umbral de cobertura
    threshold_result = check_coverage_threshold()
    all_passed = all_passed and threshold_result
    
    # Generar resumen
    generate_test_summary()
    
    # Resultado final
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    
    if all_passed:
        print("✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("✅ COBERTURA CUMPLE CON EL UMBRAL MÍNIMO DEL 60%")
        return 0
    else:
        print("❌ ALGUNAS PRUEBAS FALLARON O LA COBERTURA ES INSUFICIENTE")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)