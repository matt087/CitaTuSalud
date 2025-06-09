#!/usr/bin/env python3
"""
Script para ejecutar pruebas rápidamente después de configurar la estructura
"""

import os
import sys
import subprocess

def setup_environment():
    """Configurar el entorno para las pruebas"""
    # Agregar backend al PYTHONPATH
    backend_path = os.path.join(os.getcwd(), 'backend')
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    
    # Configurar variable de entorno
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    if backend_path not in current_pythonpath:
        if current_pythonpath:
            os.environ['PYTHONPATH'] = f"{backend_path}{os.pathsep}{current_pythonpath}"
        else:
            os.environ['PYTHONPATH'] = backend_path
    
    print(f"✅ Entorno configurado - Backend: {backend_path}")

def check_basic_imports():
    """Verificar que los imports básicos funcionan"""
    print("🔍 Verificando imports básicos...")
    
    try:
        sys.path.insert(0, 'backend')
        import api
        print("✅ api.py importado correctamente")
        
        import models
        print("✅ models.py importado correctamente")
        
        return True
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        return False

def run_simple_test():
    """Ejecutar prueba simple primero"""
    print("\n📝 Ejecutando prueba simple...")
    
    cmd = [
        sys.executable, '-m', 'pytest', 
        'tests/test_simple.py', 
        '-v', '--tb=short'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error ejecutando prueba simple: {e}")
        return False

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("\n🧪 Ejecutando todas las pruebas...")
    
    cmd = [
        sys.executable, '-m', 'pytest', 
        'tests/', 
        '-v', '--tb=short',
        '--cov=backend.api', '--cov=backend.models',
        '--cov-report=term-missing'
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error ejecutando todas las pruebas: {e}")
        return False

def list_test_files():
    """Listar archivos de prueba encontrados"""
    print("\n📂 Archivos de prueba encontrados:")
    
    if not os.path.exists('tests'):
        print("❌ Directorio tests/ no existe")
        return False
    
    test_files = []
    for file in os.listdir('tests'):
        if file.startswith('test_') and file.endswith('.py'):
            test_files.append(file)
            print(f"✅ tests/{file}")
    
    if not test_files:
        print("❌ No se encontraron archivos test_*.py en tests/")
        return False
    
    return True

def main():
    """Función principal"""
    print("⚡ EJECUTOR RÁPIDO DE PRUEBAS")
    print("=" * 50)
    
    # Configurar entorno
    setup_environment()
    
    # Verificar estructura
    if not list_test_files():
        print("\n❌ Ejecuta primero: python setup_tests.py")
        return False
    
    # Verificar imports
    if not check_basic_imports():
        print("\n❌ Problemas con imports. Revisa backend/api.py y backend/models.py")
        return False
    
    # Ejecutar prueba simple
    simple_ok = run_simple_test()
    
    if simple_ok:
        print("\n✅ Prueba simple exitosa")
        
        all_ok = run_all_tests()
        
        if all_ok:
            print("\n🎉 TODAS LAS PRUEBAS EXITOSAS")
        else:
            print("\n⚠️  Algunas pruebas fallaron")
    else:
        print("\n❌ Prueba simple falló")
        print("Revisa la configuración básica")
    
    return simple_ok

if __name__ == "__main__":
    success = main()
    if not success:
        input("\nPresiona Enter para continuar...")