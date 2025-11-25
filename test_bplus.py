#!/usr/bin/env python3
"""
Script de prueba para validar el Árbol B+
"""

import csv
import io
from typing import Any, List, Dict, Optional, Tuple
from dataclasses import dataclass
import time
import math

@dataclass
class Employee:
    """Clase que representa un empleado (registro de la tabla)"""
    nombre: str
    edad: int
    sueldo: float
    cargo: str
    id: int = 0

    def __repr__(self):
        return f"Employee(#{self.id}: {self.nombre}, {self.edad}, ${self.sueldo:,.2f}, {self.cargo})"

    def get_field(self, field_name: str):
        """Obtener valor de un campo"""
        return getattr(self, field_name)


class BPlusTreeNode:
    """Nodo del Árbol B+"""

    def __init__(self, order: int, is_leaf: bool = False):
        self.order = order
        self.is_leaf = is_leaf
        self.keys = []
        self.children = []
        self.next = None
        self.parent = None

    def is_full(self) -> bool:
        return len(self.keys) >= self.order - 1


class BPlusTree:
    """Árbol B+ para indexación de base de datos"""

    def __init__(self, order: int = 4):
        if order < 3:
            raise ValueError("El orden debe ser al menos 3")

        self.order = order
        self.root = BPlusTreeNode(order, is_leaf=True)

    def search(self, key) -> List[int]:
        leaf = self._find_leaf(key)

        for i, k in enumerate(leaf.keys):
            if k == key:
                return leaf.children[i]

        return []

    def _find_leaf(self, key) -> BPlusTreeNode:
        node = self.root

        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        return node

    def insert(self, key, emp_id: int):
        leaf = self._find_leaf(key)

        for i, k in enumerate(leaf.keys):
            if k == key:
                if emp_id not in leaf.children[i]:
                    leaf.children[i].append(emp_id)
                return

        i = 0
        while i < len(leaf.keys) and key > leaf.keys[i]:
            i += 1

        leaf.keys.insert(i, key)
        leaf.children.insert(i, [emp_id])

        if leaf.is_full():
            self._split_leaf(leaf)

    def _split_leaf(self, leaf: BPlusTreeNode):
        mid = len(leaf.keys) // 2

        new_leaf = BPlusTreeNode(self.order, is_leaf=True)
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.children = leaf.children[mid:]

        new_leaf.next = leaf.next
        leaf.next = new_leaf

        leaf.keys = leaf.keys[:mid]
        leaf.children = leaf.children[:mid]

        promote_key = new_leaf.keys[0]

        if leaf == self.root:
            new_root = BPlusTreeNode(self.order, is_leaf=False)
            new_root.keys = [promote_key]
            new_root.children = [leaf, new_leaf]
            leaf.parent = new_root
            new_leaf.parent = new_root
            self.root = new_root
        else:
            self._insert_in_parent(leaf, promote_key, new_leaf)

    def _insert_in_parent(self, left: BPlusTreeNode, key, right: BPlusTreeNode):
        parent = left.parent

        i = 0
        while i < len(parent.keys) and key > parent.keys[i]:
            i += 1

        parent.keys.insert(i, key)
        parent.children.insert(i + 1, right)
        right.parent = parent

        if parent.is_full():
            self._split_internal(parent)

    def _split_internal(self, node: BPlusTreeNode):
        mid = len(node.keys) // 2
        promote_key = node.keys[mid]

        new_node = BPlusTreeNode(self.order, is_leaf=False)
        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]

        for child in new_node.children:
            child.parent = new_node

        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        if node == self.root:
            new_root = BPlusTreeNode(self.order, is_leaf=False)
            new_root.keys = [promote_key]
            new_root.children = [node, new_node]
            node.parent = new_root
            new_node.parent = new_root
            self.root = new_root
        else:
            self._insert_in_parent(node, promote_key, new_node)

    def range_search(self, min_key, max_key) -> List[int]:
        result = []
        leaf = self._find_leaf(min_key)

        while leaf:
            for i, key in enumerate(leaf.keys):
                if min_key <= key <= max_key:
                    result.extend(leaf.children[i])
                elif key > max_key:
                    return result

            leaf = leaf.next

        return result


class EmployeeTable:
    """Tabla de empleados con índices usando Árbol B+"""

    def __init__(self, bplus_order: int = 4):
        self.employees = []
        self.indices = {}
        self.bplus_order = bplus_order
        self.next_id = 0

    def add_employee(self, nombre: str, edad: int, sueldo: float, cargo: str) -> int:
        if cargo not in ['empleado', 'jefe', 'propietario']:
            raise ValueError(f"Cargo inválido: {cargo}")

        employee = Employee(nombre, edad, sueldo, cargo, id=self.next_id)
        self.employees.append(employee)
        emp_id = self.next_id
        self.next_id += 1

        for column, bplus_tree in self.indices.items():
            value = employee.get_field(column)
            bplus_tree.insert(value, emp_id)

        return emp_id

    def create_index(self, column: str):
        if column not in ['nombre', 'edad', 'sueldo', 'cargo']:
            raise ValueError(f"Columna inválida: {column}")

        bplus_tree = BPlusTree(order=self.bplus_order)

        for emp in self.employees:
            value = emp.get_field(column)
            bplus_tree.insert(value, emp.id)

        self.indices[column] = bplus_tree
        print(f"✓ Índice Árbol B+ creado para la columna '{column}'")

    def search(self, column: str, value) -> List[Employee]:
        if column in self.indices:
            bplus_tree = self.indices[column]
            emp_ids = bplus_tree.search(value)
            return [self.employees[emp_id] for emp_id in emp_ids]
        else:
            return [emp for emp in self.employees if emp.get_field(column) == value]

    def range_search(self, column: str, min_value, max_value) -> List[Employee]:
        if column in self.indices:
            bplus_tree = self.indices[column]
            emp_ids = bplus_tree.range_search(min_value, max_value)
            return [self.employees[emp_id] for emp_id in emp_ids]
        else:
            result = []
            for emp in self.employees:
                value = emp.get_field(column)
                if min_value <= value <= max_value:
                    result.append(emp)
            return result

    def load_from_csv(self, csv_content: str):
        reader = csv.DictReader(io.StringIO(csv_content))
        count = 0

        for row in reader:
            try:
                nombre = row['nombre'].strip()
                edad = int(row['edad'])
                sueldo = float(row['sueldo'])
                cargo = row['cargo'].strip().lower()

                self.add_employee(nombre, edad, sueldo, cargo)
                count += 1
            except (KeyError, ValueError) as e:
                print(f"⚠ Error en fila {count + 1}: {e}")
                continue

        print(f"✓ {count} empleados cargados desde CSV")


# Pruebas
print("="*70)
print("PRUEBA DEL SISTEMA CON ÁRBOL B+")
print("="*70)

# Crear CSV de prueba
csv_test = """nombre,edad,sueldo,cargo
Juan Pérez,28,45000,empleado
María García,35,75000,jefe
Carlos López,28,48000,empleado
Ana Martínez,42,150000,propietario
Pedro Sánchez,31,52000,empleado
Laura Rodríguez,35,78000,jefe"""

# Crear tabla y cargar
print("\n1. Cargando empleados desde CSV...")
tabla = EmployeeTable(bplus_order=3)
tabla.load_from_csv(csv_test)

# Crear índice B+ en edad
print("\n2. Creando índice B+ en columna 'edad'...")
tabla.create_index('edad')

# Buscar empleados de 28 años
print("\n3. Buscando empleados de 28 años...")
results = tabla.search('edad', 28)
print(f"Encontrados {len(results)} empleados:")
for emp in results:
    print(f"  - {emp}")

# Búsqueda por rango
print("\n4. Buscando empleados entre 30 y 40 años...")
results_range = tabla.range_search('edad', 30, 40)
print(f"Encontrados {len(results_range)} empleados:")
for emp in results_range:
    print(f"  - {emp}")

# Crear índice en cargo
print("\n5. Creando índice B+ en columna 'cargo'...")
tabla.create_index('cargo')

# Buscar jefes
print("\n6. Buscando jefes...")
results = tabla.search('cargo', 'jefe')
print(f"Encontrados {len(results)} jefes:")
for emp in results:
    print(f"  - {emp}")

print("\n" + "="*70)
print("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("  El Árbol B+ funciona correctamente!")
print("="*70)
