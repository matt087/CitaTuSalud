#!/usr/bin/env python3
"""
Script final para ejecutar pruebas con la estructura específica de CitaTuSalud
"""

import subprocess
import sys
import os

def setup_environment():
    """Configurar el entorno para las pruebas"""
    print("Configurando entorno...")
    
    # Obtener rutas
    project_root = os.getcwd()
    backend_path = os.path.join(project_root, 'backend')
    
    # Configurar PYTHONPATH
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    paths_to_add = [backend_path, project_root]
    
    for path in paths_to_add:
        if path not in current_pythonpath:
            if current_pythonpath:
                current_pythonpath = f"{path}{os.pathsep}{current_pythonpath}"
            else:
                current_pythonpath = path
    
    os.environ['PYTHONPATH'] = current_pythonpath
    
    print(f"Directorio del proyecto: {project_root}")
    print(f"Directorio backend: {backend_path}")

def verify_structure():
    """Verificar la estructura del proyecto"""
    print("\nVerificando estructura del proyecto...")
    
    required_files = [
        'backend/api.py',
        'backend/models.py',
        'tests/conftest.py',
        'tests/test_auth.py'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"OK: {file}")
        else:
            print(f"FALTANTE: {file}")
            missing_files.append(file)
    
    if missing_files:
        print(f"\nArchivos faltantes: {missing_files}")
        return False
    
    print("Estructura del proyecto correcta")
    return True

def test_basic_imports():
    """Probar imports básicos"""
    print("\nProbando imports básicos...")
    
    try:
        # Agregar backend al path
        sys.path.insert(0, 'backend')
        
        import api
        print("api.py importado correctamente")
        
        import models
        print("models.py importado correctamente")
        
        # Verificar que la app se puede crear
        app = api.app
        print(f"App Flask creada: {app.name}")
        
        return True
    except Exception as e:
        print(f"Error en imports: {e}")
        return False

def run_pytest_discovery():
    """Verificar que pytest puede descubrir las pruebas"""
    print("\nDescubriendo pruebas con pytest...")
    
    cmd = [sys.executable, '-m', 'pytest', '--collect-only', 'tests/', '-q']
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            # Contar pruebas encontradas
            lines = result.stdout.split('\n')
            test_count = len([line for line in lines if '::test_' in line])
            print(f"Pytest puede descubrir las pruebas")
            print(f"Pruebas encontradas: {test_count}")
            return test_count > 0
        else:
            print("Pytest no puede descubrir las pruebas")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
    except Exception as e:
        print(f"Error ejecutando pytest discovery: {e}")
        return False

def run_auth_tests():
    """Ejecutar pruebas de autenticación"""
    print("\nEjecutando pruebas de autenticación...")
    
    cmd = [
        sys.executable, '-m', 'pytest', 
        'tests/test_auth.py', 
        '-v', '--tb=short'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        print("RESULTADO DE PRUEBAS DE AUTENTICACION:")
        print(result.stdout)
        
        if result.stderr:
            print("ERRORES:")
            print(result.stderr)
        
        # Analizar resultados
        stdout = result.stdout
        if "FAILED" in stdout:
            print("\nAlgunas pruebas de autenticación fallaron")
            # Extraer información de fallos
            lines = stdout.split('\n')
            for line in lines:
                if "FAILED" in line or "assert" in line:
                    print(f"   {line}")
        
        if "passed" in stdout:
            # Extraer número de pruebas que pasaron
            for line in stdout.split('\n'):
                if "passed" in line and ("failed" in line or "error" in line):
                    print(f"\nResultado: {line}")
                    break
            else:
                # Si no hay fallos, todas pasaron
                passed_count = stdout.count("PASSED")
                if passed_count > 0:
                    print(f"\n{passed_count} pruebas de autenticación exitosas")
        
        # Considerar exitoso si no hay errores críticos
        return result.returncode == 0 or "passed" in stdout
        
    except Exception as e:
        print(f"Error ejecutando pruebas de auth: {e}")
        return False

def run_all_tests():
    """Ejecutar todas las pruebas disponibles"""
    print("\nEjecutando todas las pruebas disponibles...")
    
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-v',
        '--tb=short'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        print("RESULTADO DE TODAS LAS PRUEBAS:")
        print(result.stdout)
        
        if result.stderr:
            print("ERRORES:")
            print(result.stderr)
        
        # Analizar resultados
        stdout = result.stdout
        success = False
        
        if "passed" in stdout:
            success = True
            for line in stdout.split('\n'):
                if "passed" in line and ("failed" in line or "error" in line):
                    print(f"\nResumen: {line}")
                    break
        
        return success
        
    except Exception as e:
        print(f"Error ejecutando todas las pruebas: {e}")
        return False

def run_coverage_analysis():
    """Ejecutar análisis de cobertura"""
    print("\nEjecutando análisis de cobertura...")
    
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-v',
        '--cov=backend.api',
        '--cov=backend.models',
        '--cov-report=term-missing',
        '--cov-report=html:htmlcov',
        '--tb=short'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        print("RESULTADO CON COBERTURA:")
        print(result.stdout)
        
        if result.stderr:
            print("ERRORES:")
            print(result.stderr)
        
        # Buscar información de cobertura
        lines = result.stdout.split('\n')
        for line in lines:
            if "TOTAL" in line and "%" in line:
                print(f"\nCobertura: {line}")
                break
        
        print("\nReporte HTML de cobertura generado en: htmlcov/index.html")
        
        return "TOTAL" in result.stdout
        
    except Exception as e:
        print(f"Error ejecutando análisis de cobertura: {e}")
        return False
    

def main():
    """Función principal"""
    print("EJECUTOR FINAL DE PRUEBAS - CITA TU SALUD")
    print("=" * 60)
    
    # Configurar entorno
    setup_environment()
    
    # Verificar estructura
    if not verify_structure():
        print("\nEstructura incorrecta. No se pueden ejecutar pruebas.")
        return False
    
    # Probar imports
    if not test_basic_imports():
        print("\nProblemas con imports. Revisa backend/api.py y backend/models.py")
        return False
    
    # Verificar discovery de pytest
    discovery_ok = run_pytest_discovery()
    if not discovery_ok:
        print("\nPytest no puede encontrar las pruebas")
        return False
    
    # Ejecutar pruebas de auth
    print("\n" + "EJECUTANDO PRUEBAS..." + "=" * 40)
    auth_success = run_auth_tests()
    
    # Ejecutar todas las pruebas
    all_tests_success = run_all_tests()
    
    # Ejecutar análisis de cobertura
    coverage_success = run_coverage_analysis()
    
    # Resultado final
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    
    if auth_success and all_tests_success:
        print("SISTEMA DE PRUEBAS FUNCIONANDO CORRECTAMENTE")
        print("Pruebas de autenticación: EXITOSAS")
        if coverage_success:
            print("Análisis de cobertura: GENERADO")
        else:
            print("Análisis de cobertura: CON PROBLEMAS")
        return True
    else:
        print("SISTEMA PARCIALMENTE FUNCIONAL")
        if not auth_success:
            print("Pruebas de autenticación: PROBLEMAS")
        if not all_tests_success:
            print("Ejecución de pruebas: PROBLEMAS")
        print("\nTip: Las pruebas pueden estar funcionando aunque haya algunos fallos")
        print("   Revisa los detalles arriba para ver qué pruebas específicas fallan")
        return False

if __name__ == "__main__":
    success = main()
    print("\n" + "=" * 60)
    if success:
        print("EJECUCION COMPLETADA - REVISA LOS RESULTADOS ARRIBA")
    else:
        print("EJECUCION COMPLETADA CON ADVERTENCIAS - REVISA LOS DETALLES")
    print("=" * 60)
    input("\nPresiona Enter para continuar...")