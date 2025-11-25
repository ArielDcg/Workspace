#!/usr/bin/env python3
"""
Sistema de Gestión de Tabla de Empleados con Índices
Este programa permite crear una tabla de empleados con 4 columnas:
- nombre
- edad
- sueldo
- cargo (empleado, jefe, propietario)

Y crear índices en cualquiera de estas columnas para búsquedas eficientes.
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict


class EmployeeTable:
    """
    Tabla de empleados con soporte para índices en columnas específicas.
    """

    def __init__(self):
        """Inicializa la tabla vacía y el diccionario de índices."""
        self.employees = []  # Lista de diccionarios con los datos de empleados
        self.indices = {}    # Diccionario de índices: {columna: {valor: [lista_de_índices]}}
        self.indexed_columns = set()  # Columnas que tienen índice

    def create_index(self, column_name: str):
        """
        Crea un índice para la columna especificada.

        Args:
            column_name: Nombre de la columna a indexar (nombre, edad, sueldo, cargo)
        """
        if column_name not in ['nombre', 'edad', 'sueldo', 'cargo']:
            raise ValueError(f"Columna inválida: {column_name}. Debe ser: nombre, edad, sueldo, o cargo")

        if column_name in self.indexed_columns:
            print(f"Advertencia: La columna '{column_name}' ya tiene un índice. Reconstruyendo...")

        # Crear el índice
        index = defaultdict(list)
        for idx, employee in enumerate(self.employees):
            value = employee[column_name]
            index[value].append(idx)

        self.indices[column_name] = dict(index)
        self.indexed_columns.add(column_name)
        print(f"✓ Índice creado para la columna '{column_name}'")
        print(f"  - Valores únicos: {len(self.indices[column_name])}")

    def add_employee(self, nombre: str, edad: int, sueldo: float, cargo: str):
        """
        Agrega un nuevo empleado a la tabla.

        Args:
            nombre: Nombre del empleado
            edad: Edad del empleado
            sueldo: Sueldo del empleado
            cargo: Cargo del empleado (empleado, jefe, propietario)
        """
        if cargo not in ['empleado', 'jefe', 'propietario']:
            raise ValueError(f"Cargo inválido: {cargo}. Debe ser: empleado, jefe, o propietario")

        employee = {
            'nombre': nombre,
            'edad': edad,
            'sueldo': sueldo,
            'cargo': cargo
        }

        # Agregar a la lista
        idx = len(self.employees)
        self.employees.append(employee)

        # Actualizar índices existentes
        for column in self.indexed_columns:
            value = employee[column]
            if value not in self.indices[column]:
                self.indices[column][value] = []
            self.indices[column][value].append(idx)

    def find_by_column(self, column_name: str, value: Any) -> List[Dict[str, Any]]:
        """
        Busca empleados por el valor de una columna.
        Si la columna está indexada, usa el índice. Si no, hace búsqueda lineal.

        Args:
            column_name: Nombre de la columna
            value: Valor a buscar

        Returns:
            Lista de empleados que coinciden con el valor
        """
        if column_name in self.indexed_columns:
            # Búsqueda usando índice (O(1) promedio)
            if value in self.indices[column_name]:
                indices = self.indices[column_name][value]
                return [self.employees[i] for i in indices]
            return []
        else:
            # Búsqueda lineal (O(n))
            return [emp for emp in self.employees if emp[column_name] == value]

    def find_by_age(self, edad: int) -> List[Dict[str, Any]]:
        """Busca empleados por edad."""
        return self.find_by_column('edad', edad)

    def find_by_name(self, nombre: str) -> List[Dict[str, Any]]:
        """Busca empleados por nombre."""
        return self.find_by_column('nombre', nombre)

    def find_by_position(self, cargo: str) -> List[Dict[str, Any]]:
        """Busca empleados por cargo."""
        return self.find_by_column('cargo', cargo)

    def find_by_salary(self, sueldo: float) -> List[Dict[str, Any]]:
        """Busca empleados por sueldo."""
        return self.find_by_column('sueldo', sueldo)

    def find_by_age_range(self, min_edad: int, max_edad: int) -> List[Dict[str, Any]]:
        """
        Busca empleados en un rango de edades.
        Si existe índice en edad, es más eficiente.

        Args:
            min_edad: Edad mínima (inclusive)
            max_edad: Edad máxima (inclusive)

        Returns:
            Lista de empleados en el rango de edad
        """
        if 'edad' in self.indexed_columns:
            # Usar índice para búsqueda de rango
            result = []
            for edad in range(min_edad, max_edad + 1):
                if edad in self.indices['edad']:
                    indices = self.indices['edad'][edad]
                    result.extend([self.employees[i] for i in indices])
            return result
        else:
            # Búsqueda lineal
            return [emp for emp in self.employees if min_edad <= emp['edad'] <= max_edad]

    def get_all_employees(self) -> List[Dict[str, Any]]:
        """Retorna todos los empleados."""
        return self.employees.copy()

    def show_index_stats(self):
        """Muestra estadísticas de los índices creados."""
        print("\n=== Estadísticas de Índices ===")
        if not self.indexed_columns:
            print("No hay índices creados.")
            return

        for column in self.indexed_columns:
            index = self.indices[column]
            print(f"\nColumna: {column}")
            print(f"  - Valores únicos: {len(index)}")
            print(f"  - Distribución:")
            for value, indices in sorted(index.items())[:5]:  # Mostrar solo primeros 5
                print(f"    • {value}: {len(indices)} empleado(s)")
            if len(index) > 5:
                print(f"    ... ({len(index) - 5} valores más)")

    def show_all_employees(self):
        """Muestra todos los empleados en formato tabla."""
        if not self.employees:
            print("No hay empleados en la tabla.")
            return

        print("\n=== Tabla de Empleados ===")
        print(f"{'Nombre':<20} {'Edad':<6} {'Sueldo':<12} {'Cargo':<15}")
        print("-" * 60)
        for emp in self.employees:
            print(f"{emp['nombre']:<20} {emp['edad']:<6} ${emp['sueldo']:<11,.2f} {emp['cargo']:<15}")
        print(f"\nTotal: {len(self.employees)} empleados")


def main():
    """Función principal con ejemplos de uso."""

    print("=" * 70)
    print("Sistema de Gestión de Empleados con Índices")
    print("=" * 70)

    # Crear tabla
    tabla = EmployeeTable()

    # Agregar empleados
    print("\n1. Agregando empleados...")
    tabla.add_employee("Juan Pérez", 28, 45000.00, "empleado")
    tabla.add_employee("María García", 35, 75000.00, "jefe")
    tabla.add_employee("Carlos López", 28, 48000.00, "empleado")
    tabla.add_employee("Ana Martínez", 42, 150000.00, "propietario")
    tabla.add_employee("Pedro Sánchez", 31, 52000.00, "empleado")
    tabla.add_employee("Laura Rodríguez", 35, 78000.00, "jefe")
    tabla.add_employee("Miguel Torres", 28, 46000.00, "empleado")
    tabla.add_employee("Sofia Ramírez", 39, 85000.00, "jefe")
    tabla.add_employee("Diego Flores", 25, 42000.00, "empleado")
    tabla.add_employee("Elena Castro", 45, 200000.00, "propietario")

    tabla.show_all_employees()

    # Crear índice en la columna edad
    print("\n2. Creando índice en la columna 'edad'...")
    tabla.create_index('edad')

    # Buscar empleados por edad usando índice
    print("\n3. Buscando empleados de 28 años (usando índice)...")
    empleados_28 = tabla.find_by_age(28)
    print(f"Encontrados {len(empleados_28)} empleados:")
    for emp in empleados_28:
        print(f"  - {emp['nombre']}: ${emp['sueldo']:,.2f} ({emp['cargo']})")

    # Crear índice en la columna cargo
    print("\n4. Creando índice en la columna 'cargo'...")
    tabla.create_index('cargo')

    # Buscar por cargo usando índice
    print("\n5. Buscando todos los jefes (usando índice)...")
    jefes = tabla.find_by_position('jefe')
    print(f"Encontrados {len(jefes)} jefes:")
    for emp in jefes:
        print(f"  - {emp['nombre']}: {emp['edad']} años, ${emp['sueldo']:,.2f}")

    # Búsqueda por rango de edad
    print("\n6. Buscando empleados entre 30 y 40 años (usando índice de edad)...")
    empleados_30_40 = tabla.find_by_age_range(30, 40)
    print(f"Encontrados {len(empleados_30_40)} empleados:")
    for emp in empleados_30_40:
        print(f"  - {emp['nombre']}: {emp['edad']} años, {emp['cargo']}")

    # Mostrar estadísticas de índices
    tabla.show_index_stats()

    # Demostración de índice dinámico
    print("\n7. Agregando nuevos empleados y actualizando índices automáticamente...")
    tabla.add_employee("Roberto Jiménez", 28, 47000.00, "empleado")
    tabla.add_employee("Carmen Vega", 50, 180000.00, "propietario")

    print("\n8. Buscando empleados de 28 años después de agregar nuevos (índice actualizado)...")
    empleados_28_nuevo = tabla.find_by_age(28)
    print(f"Ahora hay {len(empleados_28_nuevo)} empleados de 28 años:")
    for emp in empleados_28_nuevo:
        print(f"  - {emp['nombre']}")

    # Crear índice en nombre
    print("\n9. Creando índice en la columna 'nombre' para búsquedas rápidas...")
    tabla.create_index('nombre')

    print("\n10. Buscando empleado por nombre...")
    resultado = tabla.find_by_name("María García")
    if resultado:
        emp = resultado[0]
        print(f"Encontrado: {emp['nombre']}, {emp['edad']} años, ${emp['sueldo']:,.2f}, {emp['cargo']}")

    print("\n" + "=" * 70)
    print("Demostración completada")
    print("=" * 70)


if __name__ == "__main__":
    main()
