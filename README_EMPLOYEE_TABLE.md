# Sistema de Gestión de Empleados con Índices

Este programa implementa una tabla de empleados con soporte para índices en columnas específicas, permitiendo búsquedas eficientes.

## Características

### Estructura de la Tabla

La tabla de empleados contiene 4 columnas:

- **nombre**: Nombre del empleado (string)
- **edad**: Edad del empleado (integer)
- **sueldo**: Sueldo del empleado (float)
- **cargo**: Cargo del empleado (string: "empleado", "jefe", "propietario")

### Sistema de Índices

El programa permite crear índices en cualquier columna para optimizar búsquedas:

- **Sin índice**: Búsqueda lineal O(n)
- **Con índice**: Búsqueda por hash O(1) promedio

Los índices se actualizan automáticamente al agregar nuevos empleados.

## Uso

### Ejecutar el programa de demostración

```bash
python3 employee_table.py
```

### Uso programático

```python
from employee_table import EmployeeTable

# Crear tabla
tabla = EmployeeTable()

# Agregar empleados
tabla.add_employee("Juan Pérez", 28, 45000.00, "empleado")
tabla.add_employee("María García", 35, 75000.00, "jefe")
tabla.add_employee("Ana Martínez", 42, 150000.00, "propietario")

# Crear índice en la columna edad
tabla.create_index('edad')

# Buscar empleados de 28 años (usa el índice)
empleados = tabla.find_by_age(28)
for emp in empleados:
    print(f"{emp['nombre']}: ${emp['sueldo']:,.2f}")

# Crear índice en cargo
tabla.create_index('cargo')

# Buscar todos los jefes
jefes = tabla.find_by_position('jefe')

# Buscar en rango de edad
empleados_30_40 = tabla.find_by_age_range(30, 40)

# Mostrar todos los empleados
tabla.show_all_employees()

# Mostrar estadísticas de índices
tabla.show_index_stats()
```

## Métodos Principales

### Gestión de la Tabla

- `add_employee(nombre, edad, sueldo, cargo)`: Agrega un nuevo empleado
- `get_all_employees()`: Retorna lista de todos los empleados
- `show_all_employees()`: Muestra tabla formateada de empleados

### Gestión de Índices

- `create_index(column_name)`: Crea un índice en la columna especificada
  - Columnas válidas: 'nombre', 'edad', 'sueldo', 'cargo'
- `show_index_stats()`: Muestra estadísticas de índices creados

### Búsquedas

- `find_by_column(column_name, value)`: Búsqueda genérica por columna
- `find_by_age(edad)`: Busca por edad específica
- `find_by_name(nombre)`: Busca por nombre
- `find_by_position(cargo)`: Busca por cargo
- `find_by_salary(sueldo)`: Busca por sueldo
- `find_by_age_range(min_edad, max_edad)`: Busca en rango de edades

## Ejemplo de Salida

```
=== Tabla de Empleados ===
Nombre               Edad   Sueldo       Cargo
------------------------------------------------------------
Juan Pérez           28     $45,000.00   empleado
María García         35     $75,000.00   jefe
Carlos López         28     $48,000.00   empleado
Ana Martínez         42     $150,000.00  propietario

Total: 4 empleados

✓ Índice creado para la columna 'edad'
  - Valores únicos: 3

Buscando empleados de 28 años (usando índice)...
Encontrados 2 empleados:
  - Juan Pérez: $45,000.00 (empleado)
  - Carlos López: $48,000.00 (empleado)
```

## Ventajas del Sistema de Índices

1. **Rendimiento**: Las búsquedas en columnas indexadas son O(1) vs O(n) sin índice
2. **Flexibilidad**: Se puede indexar cualquier columna según necesidad
3. **Dinámico**: Los índices se actualizan automáticamente al agregar datos
4. **Transparente**: La API de búsqueda es la misma con o sin índices

## Casos de Uso

- **Índice en edad**: Útil para búsquedas frecuentes por edad o rangos de edad
- **Índice en cargo**: Útil para reportes por departamento o nivel jerárquico
- **Índice en nombre**: Útil para búsquedas de empleados específicos
- **Índice en sueldo**: Útil para análisis de nómina

## Implementación Técnica

- Los índices se implementan usando diccionarios de Python (hash tables)
- Cada índice mapea: `{valor_columna: [lista_de_índices_en_tabla_principal]}`
- Permite múltiples empleados con el mismo valor en una columna
- Actualización incremental de índices en O(1) por inserción

## Requisitos

- Python 3.6+
- No requiere bibliotecas externas

## Autor

Creado con Claude Code para demostrar estructuras de datos con índices.
