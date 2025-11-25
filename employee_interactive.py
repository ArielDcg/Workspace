#!/usr/bin/env python3
"""
Interfaz interactiva para el sistema de gestión de empleados
"""

from employee_table import EmployeeTable


def print_menu():
    """Muestra el menú principal."""
    print("\n" + "=" * 60)
    print("SISTEMA DE GESTIÓN DE EMPLEADOS CON ÍNDICES")
    print("=" * 60)
    print("1. Agregar empleado")
    print("2. Crear índice en columna")
    print("3. Buscar por edad")
    print("4. Buscar por nombre")
    print("5. Buscar por cargo")
    print("6. Buscar por rango de edad")
    print("7. Mostrar todos los empleados")
    print("8. Mostrar estadísticas de índices")
    print("9. Cargar datos de ejemplo")
    print("0. Salir")
    print("=" * 60)


def cargar_datos_ejemplo(tabla):
    """Carga datos de ejemplo en la tabla."""
    empleados_ejemplo = [
        ("Juan Pérez", 28, 45000.00, "empleado"),
        ("María García", 35, 75000.00, "jefe"),
        ("Carlos López", 28, 48000.00, "empleado"),
        ("Ana Martínez", 42, 150000.00, "propietario"),
        ("Pedro Sánchez", 31, 52000.00, "empleado"),
        ("Laura Rodríguez", 35, 78000.00, "jefe"),
        ("Miguel Torres", 28, 46000.00, "empleado"),
        ("Sofia Ramírez", 39, 85000.00, "jefe"),
        ("Diego Flores", 25, 42000.00, "empleado"),
        ("Elena Castro", 45, 200000.00, "propietario"),
    ]

    for nombre, edad, sueldo, cargo in empleados_ejemplo:
        tabla.add_employee(nombre, edad, sueldo, cargo)

    print(f"\n✓ Se agregaron {len(empleados_ejemplo)} empleados de ejemplo")


def agregar_empleado_interactivo(tabla):
    """Solicita datos al usuario y agrega un empleado."""
    print("\n--- Agregar Nuevo Empleado ---")
    try:
        nombre = input("Nombre: ").strip()
        if not nombre:
            print("Error: El nombre no puede estar vacío")
            return

        edad = int(input("Edad: "))
        if edad < 18 or edad > 100:
            print("Error: La edad debe estar entre 18 y 100")
            return

        sueldo = float(input("Sueldo: "))
        if sueldo < 0:
            print("Error: El sueldo no puede ser negativo")
            return

        print("Cargos disponibles: empleado, jefe, propietario")
        cargo = input("Cargo: ").strip().lower()
        if cargo not in ['empleado', 'jefe', 'propietario']:
            print("Error: Cargo inválido")
            return

        tabla.add_employee(nombre, edad, sueldo, cargo)
        print(f"✓ Empleado {nombre} agregado exitosamente")

    except ValueError as e:
        print(f"Error: Entrada inválida - {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


def crear_indice_interactivo(tabla):
    """Solicita la columna y crea un índice."""
    print("\n--- Crear Índice ---")
    print("Columnas disponibles: nombre, edad, sueldo, cargo")
    columna = input("Columna a indexar: ").strip().lower()

    try:
        tabla.create_index(columna)
    except ValueError as e:
        print(f"Error: {e}")


def buscar_por_edad_interactivo(tabla):
    """Busca empleados por edad."""
    print("\n--- Buscar por Edad ---")
    try:
        edad = int(input("Edad a buscar: "))
        resultados = tabla.find_by_age(edad)

        if resultados:
            print(f"\nEncontrados {len(resultados)} empleado(s):")
            for emp in resultados:
                print(f"  - {emp['nombre']}: ${emp['sueldo']:,.2f} ({emp['cargo']})")
        else:
            print("No se encontraron empleados con esa edad")

    except ValueError:
        print("Error: Debe ingresar un número válido")


def buscar_por_nombre_interactivo(tabla):
    """Busca empleados por nombre."""
    print("\n--- Buscar por Nombre ---")
    nombre = input("Nombre a buscar: ").strip()

    resultados = tabla.find_by_name(nombre)

    if resultados:
        print(f"\nEncontrados {len(resultados)} empleado(s):")
        for emp in resultados:
            print(f"  - {emp['nombre']}: {emp['edad']} años, ${emp['sueldo']:,.2f}, {emp['cargo']}")
    else:
        print("No se encontró ningún empleado con ese nombre")


def buscar_por_cargo_interactivo(tabla):
    """Busca empleados por cargo."""
    print("\n--- Buscar por Cargo ---")
    print("Cargos disponibles: empleado, jefe, propietario")
    cargo = input("Cargo a buscar: ").strip().lower()

    if cargo not in ['empleado', 'jefe', 'propietario']:
        print("Error: Cargo inválido")
        return

    resultados = tabla.find_by_position(cargo)

    if resultados:
        print(f"\nEncontrados {len(resultados)} {cargo}(s):")
        for emp in resultados:
            print(f"  - {emp['nombre']}: {emp['edad']} años, ${emp['sueldo']:,.2f}")
    else:
        print(f"No se encontraron {cargo}s")


def buscar_rango_edad_interactivo(tabla):
    """Busca empleados en un rango de edad."""
    print("\n--- Buscar por Rango de Edad ---")
    try:
        min_edad = int(input("Edad mínima: "))
        max_edad = int(input("Edad máxima: "))

        if min_edad > max_edad:
            print("Error: La edad mínima no puede ser mayor que la máxima")
            return

        resultados = tabla.find_by_age_range(min_edad, max_edad)

        if resultados:
            print(f"\nEncontrados {len(resultados)} empleado(s) entre {min_edad} y {max_edad} años:")
            for emp in resultados:
                print(f"  - {emp['nombre']}: {emp['edad']} años, {emp['cargo']}")
        else:
            print(f"No se encontraron empleados en el rango {min_edad}-{max_edad} años")

    except ValueError:
        print("Error: Debe ingresar números válidos")


def main():
    """Función principal del programa interactivo."""
    tabla = EmployeeTable()

    while True:
        print_menu()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == '1':
            agregar_empleado_interactivo(tabla)

        elif opcion == '2':
            crear_indice_interactivo(tabla)

        elif opcion == '3':
            buscar_por_edad_interactivo(tabla)

        elif opcion == '4':
            buscar_por_nombre_interactivo(tabla)

        elif opcion == '5':
            buscar_por_cargo_interactivo(tabla)

        elif opcion == '6':
            buscar_rango_edad_interactivo(tabla)

        elif opcion == '7':
            tabla.show_all_employees()

        elif opcion == '8':
            tabla.show_index_stats()

        elif opcion == '9':
            cargar_datos_ejemplo(tabla)

        elif opcion == '0':
            print("\n¡Hasta luego!")
            break

        else:
            print("\nOpción inválida. Por favor intente de nuevo.")

        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()
