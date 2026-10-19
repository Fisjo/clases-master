# Clase SQL 1 · Crear y modificar tablas, insertar y consultar datos

En esta clase se usa el entorno **PostgreSQL + pgAdmin** que se dejó preparado con Docker Compose (ver [clase-docker3](../../docker/clase-docker3/README.md)). Se trabaja sobre una única tabla, `peliculas`, y se recorre el ciclo básico de SQL:

1. **Crear** una tabla (`CREATE TABLE`).
2. **Modificarla** (`ALTER TABLE`: añadir, renombrar, borrar columnas y cambiar tipos).
3. **Insertar** filas (`INSERT INTO`).
4. **Consultar** los datos (`SELECT`): columnas, alias, filtros, ordenación, funciones, agregados y agrupaciones.
5. **Actualizar y borrar** filas (`UPDATE`, `DELETE`).

Todo se ejecuta como un script, de arriba abajo, en la herramienta de consultas de pgAdmin.

## Índice

1. [Crear la tabla](#1-crear-la-tabla)
2. [Modificar la tabla con ALTER TABLE](#2-modificar-la-tabla-con-alter-table)
3. [Insertar datos](#3-insertar-datos)
4. [Consultar con SELECT](#4-consultar-con-select)
5. [Filtrar con WHERE](#5-filtrar-con-where)
6. [Ordenar y limitar](#6-ordenar-y-limitar)
7. [Modificar y borrar datos: UPDATE y DELETE](#7-modificar-y-borrar-datos-update-y-delete)
8. [Funciones y operadores sobre columnas](#8-funciones-y-operadores-sobre-columnas)
9. [Agregados y GROUP BY](#9-agregados-y-group-by)
10. [Qué ocurre al ejecutar el script entero](#10-qué-ocurre-al-ejecutar-el-script-entero)
11. [Resumen de sintaxis](#11-resumen-de-sintaxis)

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
SELECT * FROM peliculas;                      -- todas las columnas y filas
SELECT titulo, genero FROM peliculas;         -- solo las columnas indicadas
SELECT titulo AS nombre_pelicula FROM peliculas;  -- alias de columna
```

- `*` significa «todas las columnas»; sin `WHERE` se devuelven **todas las filas**.
- Es mejor pedir solo las columnas que hacen falta.
- `AS` da un **alias** al nombre de la columna en el resultado (no cambia la tabla).
- `SELECT DISTINCT genero FROM peliculas;` elimina duplicados: devuelve cada género una sola vez.

Orden lógico en que se escribe una consulta:

```
SELECT … FROM … WHERE … GROUP BY … HAVING … ORDER BY … LIMIT …
```

## 5. Filtrar con WHERE

`WHERE` deja pasar solo las filas que cumplen una condición.

```sql
SELECT titulo, valoracion
FROM peliculas
WHERE disponible = TRUE
    AND valoracion > 8;               -- disponibles y mejor valoradas que 8

SELECT titulo, genero
FROM peliculas
WHERE genero = 'Thriller';            -- igualdad con texto

SELECT titulo, genero
FROM peliculas
WHERE genero LIKE '%ficc%';           -- contiene «ficc»

SELECT titulo, genero
FROM peliculas
WHERE genero NOT LIKE '%Terror%';     -- no contiene «Terror»

SELECT titulo, valoracion
FROM peliculas
WHERE valoracion BETWEEN 8 AND 9;     -- rango, extremos incluidos
```

| Herramienta | Qué hace |
|---|---|
| `=`, `<>`, `>`, `<`, `>=`, `<=` | Comparaciones |
| `AND`, `OR`, `NOT` | Combinar condiciones |
| `LIKE` / `NOT LIKE` | Búsqueda de patrones en texto. `%` = cualquier cantidad de caracteres, `_` = uno solo |
| `BETWEEN a AND b` | Rango con **ambos extremos incluidos** (`BETWEEN 7.5 AND 8.5` ≡ `>= 7.5 AND <= 8.5`) |

Notas:
- El texto va entre **comillas simples** y es sensible a mayúsculas en `=` y `LIKE` (para ignorarlas existe `ILIKE`).
- `NOT LIKE '%Terror%'` devuelve todas las filas porque no hay ningún género «Terror» en los datos.

## 6. Ordenar y limitar

```sql
SELECT titulo, valoracion
FROM peliculas
WHERE valoracion > 8
ORDER BY valoracion DESC;             -- de mayor a menor

SELECT titulo, disponible, valoracion
FROM peliculas
ORDER BY disponible, valoracion ASC;  -- varios criterios

SELECT * FROM peliculas LIMIT 5;      -- solo 5 filas
```

- `ORDER BY` ordena el resultado; `ASC` (por defecto) ascendente, `DESC` descendente. Con varias columnas, la segunda desempata la primera.
- En `ORDER BY disponible`, `FALSE` va antes que `TRUE`, así que primero salen las no disponibles.
- `LIMIT n` corta el resultado a `n` filas (normalmente junto a `ORDER BY` para «los n mejores»).
- Se puede ordenar por un **alias** definido en el `SELECT` (`ORDER BY valoracion_porciento`).

## 7. Modificar y borrar datos: UPDATE y DELETE

```sql
DELETE FROM peliculas
WHERE titulo = 'El Padrino';

UPDATE peliculas
SET valoracion = 9.5
WHERE titulo = 'Interestelar';

UPDATE peliculas
SET genero = 'Ciencia ficción'
WHERE id = 6;

UPDATE peliculas
SET disponible = FALSE
WHERE valoracion = (
    SELECT MIN(valoracion)
    FROM peliculas
);
```

- `DELETE FROM t WHERE …` borra las filas que cumplen la condición.
- `UPDATE t SET columna = valor WHERE …` cambia columnas de las filas que cumplen la condición. Se pueden cambiar varias separándolas con comas.
- **⚠ Sin `WHERE`, `UPDATE` y `DELETE` afectan a TODAS las filas.** Conviene probar antes con un `SELECT` con el mismo `WHERE`.
- Filtrar por `id` es lo más seguro, porque es único; por `titulo` podría afectar a varias filas.
- El último `UPDATE` usa una **subconsulta**: `(SELECT MIN(valoracion) FROM peliculas)` se evalúa primero y devuelve la valoración más baja; así se marca como no disponible la película peor valorada (con estos datos, `Cars`, 7.3).
- Efecto con estos datos: `El Padrino` desaparece (quedan 23 películas); `Interestelar` ya tenía 9.5 y `Matrix` (id 6) ya era «Ciencia ficción», así que esos dos `UPDATE` no cambian nada visible.

## 8. Funciones y operadores sobre columnas

```sql
SELECT titulo || ' -- Valoración: ' || valoracion AS nombre_y_valoracion
FROM peliculas;                                   -- concatenar con ||

SELECT titulo || ' (' || anio_estreno || ')' AS titulo_anio_estreno
FROM peliculas;                                   -- «Matrix (1999)»

SELECT UPPER(titulo) FROM peliculas LIMIT 10;     -- mayúsculas
SELECT DISTINCT LOWER(genero) FROM peliculas LIMIT 10;  -- minúsculas sin repetidos

SELECT COALESCE(genero, 'Sin genero') FROM peliculas;   -- valor alternativo si es NULL

SELECT valoracion, valoracion * 10 AS valoracion_porciento
FROM peliculas
ORDER BY valoracion_porciento DESC;

SELECT valoracion, valoracion / 2 AS valoracion_mitad
FROM peliculas
ORDER BY valoracion_mitad DESC;

SELECT valoracion, ROUND(valoracion) AS valoracion_redondeada
FROM peliculas
ORDER BY valoracion_redondeada DESC;
```

| Elemento | Función |
|---|---|
| `a \|\| b` | Concatena texto (los números se convierten solos) |
| `UPPER(x)`, `LOWER(x)` | Mayúsculas / minúsculas |
| `COALESCE(x, alternativa)` | Primer valor que no sea `NULL`. Aquí no tiene efecto visible porque `genero` es `NOT NULL`, pero protege columnas que admiten `NULL` |
| `+ - * /` | Aritmética sobre columnas, fila a fila |
| `ROUND(x)`, `ROUND(x, n)` | Redondea a entero o a `n` decimales |

Los cálculos se hacen en la consulta: **no modifican la tabla**. Como `anio_estreno` es ahora `VARCHAR`, se concatena sin conversión.

## 9. Agregados y GROUP BY

Las **funciones de agregado** reducen varias filas a un único valor.

```sql
SELECT COUNT(*) AS total_peliculas,
       ROUND(AVG(valoracion), 3) AS media_valoracion,
       MAX(valoracion) AS maximo_valoracion,
       MIN(valoracion) AS minimo_valoracion
FROM peliculas;
```

Con los datos tras el `DELETE`: 23 películas, media 8,491, máximo 9,5 y mínimo 7,3.

| Función | Devuelve |
|---|---|
| `COUNT(*)` | Número de filas |
| `AVG(x)` | Media |
| `MAX(x)` / `MIN(x)` | Máximo / mínimo |
| `SUM(x)` | Suma |

### GROUP BY

`GROUP BY` forma un grupo por cada valor distinto y calcula el agregado dentro de cada grupo.

```sql
SELECT genero, COUNT(*) AS cantidad
FROM peliculas
GROUP BY genero
ORDER BY cantidad DESC;

SELECT genero, ROUND(AVG(valoracion), 2) AS media_valoracion
FROM peliculas
GROUP BY genero
ORDER BY media_valoracion DESC;
```

Regla: toda columna del `SELECT` que no sea un agregado debe aparecer en el `GROUP BY`. Con estos datos, `Animación` es el género más repetido (5 películas).

### HAVING frente a WHERE

```sql
SELECT genero, COUNT(*) AS cantidad
FROM peliculas
GROUP BY genero
HAVING COUNT(*) > 2;                 -- grupos con más de 2 películas

SELECT genero, COUNT(*) AS cantidad
FROM peliculas
WHERE valoracion > 8                 -- primero filtra filas…
GROUP BY genero
HAVING COUNT(*) > 2;                 -- …luego filtra grupos
```

| | `WHERE` | `HAVING` |
|---|---|---|
| Filtra | Filas, **antes** de agrupar | Grupos, **después** de agrupar |
| Admite agregados | No | Sí (`COUNT(*) > 2`) |

En ambas consultas salen Animación, Acción, Drama y Ciencia ficción; en la segunda los conteos son de películas con valoración > 8 (Animación 4, el resto 3).

## 10. Qué ocurre al ejecutar el script entero

Se ejecuta secuencialmente y **se detiene en el primer error**:

1. `CREATE TABLE IF NOT EXISTS` crea la tabla (o no hace nada si ya existe).
2. `DROP COLUMN director` **falla**, porque la columna `director` no existe en la definición inicial: *column "director" of relation "peliculas" does not exist*. Para que el script no se detenga se puede usar `DROP COLUMN IF EXISTS director`, o ejecutar las sentencias de una en una (seleccionando cada una en pgAdmin) para ver el efecto de cada paso.
3. Si se va ejecutando sentencia a sentencia, `ADD COLUMN`/`ALTER COLUMN`, `RENAME` y el segundo `DROP COLUMN` funcionan en ese orden, y después los `INSERT`, los `SELECT`, `DELETE` y `UPDATE`.
4. Si se vuelve a ejecutar el script sobre una tabla que ya tiene datos, los `INSERT` **duplican** las filas (los ids siguen creciendo), el `ADD COLUMN director NOT NULL` falla al haber ya filas y el `DELETE` del principio ya no recupera el estado inicial. Para empezar de cero: `DROP TABLE peliculas;`.

## 11. Resumen de sintaxis

| Sentencia / cláusula | Para qué |
|---|---|
| `CREATE TABLE [IF NOT EXISTS] t (...)` | Crear una tabla |
| `ALTER TABLE t ADD / DROP / ALTER / RENAME COLUMN ...` | Modificar su estructura |
| `INSERT INTO t (cols) VALUES (...), (...)` | Insertar una o varias filas |
| `SELECT cols FROM t` | Consultar datos |
| `AS alias` | Renombrar una columna en el resultado |
| `DISTINCT` | Quitar duplicados |
| `WHERE` con `AND`, `OR`, `LIKE`, `BETWEEN` | Filtrar filas |
| `ORDER BY col [ASC\|DESC]` | Ordenar |
| `LIMIT n` | Limitar filas |
| `UPDATE t SET c = v WHERE ...` | Modificar filas |
| `DELETE FROM t WHERE ...` | Borrar filas |
| `\|\|`, `UPPER`, `LOWER`, `COALESCE`, `ROUND` | Funciones sobre valores |
| `COUNT`, `AVG`, `MAX`, `MIN`, `SUM` | Agregados |
| `GROUP BY` / `HAVING` | Agrupar y filtrar grupos |
| `DROP TABLE t` | Eliminar la tabla entera |

Tipos vistos: `BIGINT`, `INTEGER`, `VARCHAR(n)`, `NUMERIC(p,s)`, `BOOLEAN`, `TIMESTAMPTZ`.
