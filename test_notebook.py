#!/usr/bin/env python3
"""
Script de prueba para validar el código del notebook
"""

import csv
import io
from typing import Any, List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import time

@dataclass
class Employee:
    """Clase que representa un empleado (registro de la tabla)"""
    nombre: str
    edad: int
    sueldo: float
    cargo: str

    def __repr__(self):
        return f"Employee({self.nombre}, {self.edad}, ${self.sueldo:,.2f}, {self.cargo})"

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'edad': self.edad,
            'sueldo': self.sueldo,
            'cargo': self.cargo
        }


class LinkedListNode:
    """Nodo para lista enlazada simple"""
    def __init__(self, data: Employee):
        self.data = data
        self.next = None


class LinkedList:
    """Lista enlazada simple para almacenar empleados"""
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, employee: Employee):
        """Agregar empleado al final de la lista"""
        new_node = LinkedListNode(employee)

        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

        self.size += 1
        return self.size - 1

    def get(self, index: int) -> Optional[Employee]:
        """Obtener empleado por índice"""
        if index < 0 or index >= self.size:
            return None

        current = self.head
        for _ in range(index):
            current = current.next

        return current.data

    def to_list(self) -> List[Employee]:
        """Convertir lista enlazada a lista de Python"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __len__(self):
        return self.size


class BSTNode:
    """Nodo de Árbol Binario de Búsqueda"""
    def __init__(self, key, indices=None):
        self.key = key
        self.indices = indices if indices else []
        self.left = None
        self.right = None
        self.height = 1


class BinarySearchTree:
    """Árbol Binario de Búsqueda para índices"""
    def __init__(self):
        self.root = None
        self.node_count = 0

    def insert(self, key, index: int):
        """Insertar un valor con su índice en el BST"""
        if self.root is None:
            self.root = BSTNode(key, [index])
            self.node_count += 1
        else:
            self._insert_recursive(self.root, key, index)

    def _insert_recursive(self, node: BSTNode, key, index: int):
        """Inserción recursiva en BST"""
        if key == node.key:
            node.indices.append(index)
        elif key < node.key:
            if node.left is None:
                node.left = BSTNode(key, [index])
                self.node_count += 1
            else:
                self._insert_recursive(node.left, key, index)
        else:
            if node.right is None:
                node.right = BSTNode(key, [index])
                self.node_count += 1
            else:
                self._insert_recursive(node.right, key, index)

    def search(self, key) -> List[int]:
        """Buscar un valor en el BST y retornar lista de índices"""
        node = self._search_recursive(self.root, key)
        return node.indices if node else []

    def _search_recursive(self, node: Optional[BSTNode], key) -> Optional[BSTNode]:
        """Búsqueda recursiva en BST"""
        if node is None or node.key == key:
            return node

        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def range_search(self, min_key, max_key) -> List[int]:
        """Buscar valores en un rango [min_key, max_key]"""
        result = []
        self._range_search_recursive(self.root, min_key, max_key, result)
        return result

    def _range_search_recursive(self, node: Optional[BSTNode], min_key, max_key, result: List[int]):
        """Búsqueda de rango recursiva en BST"""
        if node is None:
            return

        if min_key <= node.key <= max_key:
            result.extend(node.indices)

        if min_key < node.key:
            self._range_search_recursive(node.left, min_key, max_key, result)

        if max_key > node.key:
            self._range_search_recursive(node.right, min_key, max_key, result)


class HashTableNode:
    """Nodo para manejar colisiones mediante encadenamiento"""
    def __init__(self, key, indices=None):
        self.key = key
        self.indices = indices if indices else []
        self.next = None


class HashTable:
    """Tabla Hash con encadenamiento para manejar colisiones"""
    def __init__(self, size=100):
        self.size = size
        self.table = [None] * size
        self.count = 0

    def _hash(self, key) -> int:
        """Función hash"""
        if isinstance(key, str):
            hash_value = 0
            for char in key:
                hash_value = (hash_value * 31 + ord(char)) % self.size
            return hash_value
        elif isinstance(key, (int, float)):
            return int(key) % self.size
        else:
            return hash(key) % self.size

    def insert(self, key, index: int):
        """Insertar un par clave-índice en la tabla hash"""
        hash_index = self._hash(key)

        if self.table[hash_index] is None:
            self.table[hash_index] = HashTableNode(key, [index])
            self.count += 1
        else:
            current = self.table[hash_index]

            while current:
                if current.key == key:
                    current.indices.append(index)
                    return
                if current.next is None:
                    break
                current = current.next

            current.next = HashTableNode(key, [index])
            self.count += 1

    def search(self, key) -> List[int]:
        """Buscar una clave en la tabla hash"""
        hash_index = self._hash(key)
        current = self.table[hash_index]

        while current:
            if current.key == key:
                return current.indices
            current = current.next

        return []


class IndexType(Enum):
    """Tipo de estructura de datos para el índice"""
    BST = "bst"
    HASH = "hash"


class EmployeeTable:
    """Tabla de empleados con soporte para índices usando estructuras de datos"""

    def __init__(self):
        self.employees = LinkedList()
        self.indices = {}

    def add_employee(self, nombre: str, edad: int, sueldo: float, cargo: str) -> int:
        """Agregar empleado a la tabla"""
        if cargo not in ['empleado', 'jefe', 'propietario']:
            raise ValueError(f"Cargo inválido: {cargo}")

        employee = Employee(nombre, edad, sueldo, cargo)
        index = self.employees.append(employee)

        for column, (index_type, structure) in self.indices.items():
            value = getattr(employee, column)
            structure.insert(value, index)

        return index

    def create_index(self, column: str, index_type: IndexType = IndexType.HASH):
        """Crear índice en una columna específica"""
        if column not in ['nombre', 'edad', 'sueldo', 'cargo']:
            raise ValueError(f"Columna inválida: {column}")

        if index_type == IndexType.BST:
            structure = BinarySearchTree()
        else:
            structure = HashTable()

        all_employees = self.employees.to_list()
        for idx, employee in enumerate(all_employees):
            value = getattr(employee, column)
            structure.insert(value, idx)

        self.indices[column] = (index_type, structure)

        type_name = "BST" if index_type == IndexType.BST else "Hash Table"
        print(f"✓ Índice tipo {type_name} creado para la columna '{column}'")

    def search(self, column: str, value) -> List[Employee]:
        """Buscar empleados por valor en una columna"""
        if column in self.indices:
            _, structure = self.indices[column]
            indices = structure.search(value)
            return [self.employees.get(i) for i in indices]
        else:
            result = []
            all_employees = self.employees.to_list()
            for emp in all_employees:
                if getattr(emp, column) == value:
                    result.append(emp)
            return result

    def load_from_csv(self, csv_content: str):
        """Cargar empleados desde contenido CSV"""
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
print("PRUEBA DEL SISTEMA DE EMPLEADOS CON ESTRUCTURAS DE DATOS")
print("="*70)

# Crear CSV de prueba
csv_test = """nombre,edad,sueldo,cargo
Juan Pérez,28,45000,empleado
María García,35,75000,jefe
Carlos López,28,48000,empleado
Ana Martínez,42,150000,propietario"""

# Crear tabla y cargar
print("\n1. Cargando empleados desde CSV...")
tabla = EmployeeTable()
tabla.load_from_csv(csv_test)

# Crear índice BST en edad
print("\n2. Creando índice BST en columna 'edad'...")
tabla.create_index('edad', IndexType.BST)

# Buscar empleados de 28 años
print("\n3. Buscando empleados de 28 años...")
results = tabla.search('edad', 28)
print(f"Encontrados {len(results)} empleados:")
for emp in results:
    print(f"  - {emp}")

# Crear índice Hash en cargo
print("\n4. Creando índice Hash en columna 'cargo'...")
tabla.create_index('cargo', IndexType.HASH)

# Buscar jefes
print("\n5. Buscando jefes...")
results = tabla.search('cargo', 'jefe')
print(f"Encontrados {len(results)} jefes:")
for emp in results:
    print(f"  - {emp}")

print("\n" + "="*70)
print("✓ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("="*70)
