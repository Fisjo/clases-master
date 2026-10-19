# Clase SQL 1 · Crear y modificar tablas, insertar y consultar datos

En esta clase se usa el entorno **PostgreSQL + pgAdmin** que se dejó preparado con Docker Compose (ver [clase-docker3](../clase-docker3/README.md)). Se trabaja sobre una única tabla, `peliculas`, y se recorre el ciclo básico de SQL:

1. **Crear** una tabla (`CREATE TABLE`).
2. **Modificarla** (`ALTER TABLE`: añadir, renombrar, borrar columnas y cambiar tipos).
3. **Insertar** filas (`INSERT INTO`).
4. **Consultar** los datos (`SELECT`).

Todo se ejecuta como un script, de arriba abajo, en la herramienta de consultas de pgAdmin.

## Índice

- [Clase SQL 1 · Crear y modificar tablas, insertar y consultar datos](#clase-sql-1--crear-y-modificar-tablas-insertar-y-consultar-datos)
  - [Índice](#índice)
  - [1. Crear la tabla](#1-crear-la-tabla)
    - [Restricciones usadas](#restricciones-usadas)
  - [2. Modificar la tabla con ALTER TABLE](#2-modificar-la-tabla-con-alter-table)
  - [3. Insertar datos](#3-insertar-datos)
  - [4. Consultar con SELECT](#4-consultar-con-select)
  - [5. Qué ocurre al ejecutar el script entero](#5-qué-ocurre-al-ejecutar-el-script-entero)
  - [6. Resumen de sintaxis](#6-resumen-de-sintaxis)

---

## 1. Crear la tabla

```sql
CREATE TABLE IF NOT EXISTS peliculas(
    id            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    titulo        VARCHAR(100) NOT NULL,
    genero        VARCHAR(30)  NOT NULL,
    valoracion    NUMERIC(3,1) NOT NULL,
    anio_estreno  INTEGER      NOT NULL,
    disponible    BOOLEAN      NOT NULL DEFAULT TRUE,
    fecha_alta    TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

`CREATE TABLE` define el **esquema**: nombre de cada columna, su **tipo de dato** y sus **restricciones**. `IF NOT EXISTS` evita error si la tabla ya existe.

| Columna | Tipo | Significado |
|---|---|---|
| `id` | `BIGINT` + `GENERATED ALWAYS AS IDENTITY` + `PRIMARY KEY` | Número entero que la base genera sola y automáticamente (1, 2, 3…). Al ser clave primaria identifica cada fila de forma única |
| `titulo` | `VARCHAR(100)` | Texto de hasta 100 caracteres |
| `genero` | `VARCHAR(30)` | Texto de hasta 30 caracteres |
| `valoracion` | `NUMERIC(3,1)` | Decimal exacto con 3 dígitos en total y 1 decimal (de 0.0 a 99.9; p. ej. `9.2`) |
| `anio_estreno` | `INTEGER` | Año como número entero |
| `disponible` | `BOOLEAN` | `TRUE`/`FALSE` |
| `fecha_alta` | `TIMESTAMPTZ` | Fecha y hora **con zona horaria** |

### Restricciones usadas

- `NOT NULL`: la columna no admite valores vacíos; la inserción falla si falta el dato.
- `DEFAULT valor`: valor que se usa si no se indica ninguno al insertar. `disponible` es `TRUE` por defecto y `fecha_alta` toma el instante actual (`CURRENT_TIMESTAMP`).
- `PRIMARY KEY`: unicidad y no nulo, para identificar filas.
- `GENERATED ALWAYS AS IDENTITY`: el `id` lo asigna siempre la base de datos; no se puede insertar a mano.

## 2. Modificar la tabla con ALTER TABLE

`ALTER TABLE` cambia la estructura de una tabla que ya existe, sin recrearla.

```sql
-- Borrar una columna
ALTER TABLE peliculas
    DROP COLUMN director;

-- Añadir una columna y cambiar el tipo de otra, en una sola sentencia
ALTER TABLE peliculas
    ADD COLUMN director VARCHAR(50) NOT NULL,
    ALTER COLUMN anio_estreno TYPE VARCHAR(4);

-- Renombrar una columna
ALTER TABLE peliculas
    RENAME COLUMN director TO director_principal;

-- Borrar de nuevo esa columna
ALTER TABLE peliculas
    DROP COLUMN director_principal;
```

| Operación | Sintaxis |
|---|---|
| Añadir columna | `ADD COLUMN nombre tipo [restricciones]` |
| Borrar columna | `DROP COLUMN nombre` |
| Cambiar tipo | `ALTER COLUMN nombre TYPE nuevo_tipo` |
| Renombrar columna | `RENAME COLUMN viejo TO nuevo` |

Observaciones importantes:

- Se pueden **encadenar varias acciones** en un mismo `ALTER TABLE`, separadas por comas (como en la segunda sentencia).
- `anio_estreno` pasa de `INTEGER` a `VARCHAR(4)`: el año se guardará como **texto** de 4 caracteres, por eso los `INSERT` posteriores lo escriben entre comillas (`'1972'`). Cambiar el tipo funciona porque Postgres sabe convertir enteros a texto; la dirección contraria (texto → número) exigiría `USING`.
- Añadir una columna `NOT NULL` sin `DEFAULT` solo funciona si la tabla **está vacía** (aquí lo está, todavía no hay filas); con filas existentes fallaría porque no habría valor para rellenarlas.
- Al final la columna `director` desaparece, así que el esquema vuelve al de la creación, salvo que `anio_estreno` es ahora `VARCHAR(4)`.

## 3. Insertar datos

```sql
INSERT INTO peliculas (titulo, genero, valoracion, anio_estreno, disponible, fecha_alta) VALUES
    ('El Padrino', 'Crimen', 9.2, '1972', TRUE, '2025-01-10 10:00:00+00'),
    ('Pulp Fiction', 'Crimen', 8.9, '1994', TRUE, '2025-01-11 11:30:00+00'),
    ...;
```

- Se listan las **columnas** a rellenar y, tras `VALUES`, una **tupla por fila**, separadas por comas: una sola sentencia inserta muchas filas.
- Los valores van en el mismo orden que las columnas. Texto y fechas entre comillas simples; números y booleanos sin comillas.
- **No se incluye `id`**: lo genera la identidad.
- `fecha_alta` se da explícitamente aquí (con `+00` = UTC) en lugar de usar el valor por defecto; si se omitiera, tomaría el momento actual.
- Hay dos bloques de inserción: el primero con 20 películas clásicas (de `El Padrino` a `El Laberinto del Fauno`) y el segundo con 4 más (`Oppenheimer`, `La Odisea`, `Cars`, `Cómo entrenar a tu dragón`). En total, **24 filas** con géneros como Crimen, Acción, Drama, Ciencia ficción, Animación, Thriller, Fantasía…
- Varias películas tienen `disponible = FALSE` (Forrest Gump, Titanic, La lista de Schindler, Salvar al soldado Ryan, El Laberinto del Fauno), útil para practicar filtros después.

## 4. Consultar con SELECT

```sql
SELECT * FROM peliculas;
```

`SELECT` lee datos; `*` significa «todas las columnas» y, sin `WHERE`, devuelve **todas las filas**. Es la forma de comprobar que el script ha hecho lo esperado. Es la base sobre la que se irán añadiendo filtros (`WHERE`), ordenación (`ORDER BY`), agregados (`COUNT`, `AVG`, `GROUP BY`), etc.

## 5. Qué ocurre al ejecutar el script entero

Se ejecuta secuencialmente y **se detiene en el primer error**:

1. `CREATE TABLE IF NOT EXISTS` crea la tabla (o no hace nada si ya existe).
2. `DROP COLUMN director` **falla**, porque la columna `director` no existe en la definición inicial: *column "director" of relation "peliculas" does not exist*. Para que el script no se detenga se puede usar `DROP COLUMN IF EXISTS director`, o ejecutar las sentencias de una en una (seleccionando cada una en pgAdmin) para ver el efecto de cada paso.
3. Si se va ejecutando sentencia a sentencia, `ADD COLUMN`/`ALTER COLUMN`, `RENAME` y el segundo `DROP COLUMN` funcionan en ese orden, y después los `INSERT` y el `SELECT`.
4. Si se vuelve a ejecutar el script sobre una tabla que ya tiene datos, los `INSERT` **duplican** las filas (los ids siguen creciendo) y el `ADD COLUMN director NOT NULL` fallaría al haber ya filas. Para empezar de cero: `DROP TABLE peliculas;`.

## 6. Resumen de sintaxis

| Sentencia | Para qué |
|---|---|
| `CREATE TABLE [IF NOT EXISTS] t (...)` | Crear una tabla |
| `ALTER TABLE t ADD COLUMN ...` | Añadir columna |
| `ALTER TABLE t DROP COLUMN ...` | Borrar columna |
| `ALTER TABLE t ALTER COLUMN c TYPE ...` | Cambiar tipo |
| `ALTER TABLE t RENAME COLUMN a TO b` | Renombrar columna |
| `INSERT INTO t (cols) VALUES (...), (...)` | Insertar una o varias filas |
| `SELECT * FROM t` | Ver todos los datos |
| `DROP TABLE t` | Eliminar la tabla entera |

Tipos vistos: `BIGINT`, `INTEGER`, `VARCHAR(n)`, `NUMERIC(p,s)`, `BOOLEAN`, `TIMESTAMPTZ`.
