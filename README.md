# Repositorio de clases de Máster de IA, Data & Cloud @ EDEM Escuela de Empresarios

Este repositorio reúne los ejercicios y apuntes de las clases del máster: Python, Git y GitHub Actions, Docker y SQL con PostgreSQL, además de un reto final que integra SQL, Python y Docker. No se trata de un proyecto de producción, sino de un espacio para practicar y documentar cada clase (casi todas tienen su propio `README.md`).

## Estructura del repositorio

- `python/clase-python1/clase1.py`: archivo principal de práctica de Python. Aquí se trabajan conceptos básicos como:
  - variables
  - cadenas de texto
  - listas y diccionarios
  - tuplas
  - operadores
  - condicionales
  - comparaciones y asignaciones

- `python/clase-python2/clase2.py`: segunda clase de Python. Se trabajan:
  - sets
  - repaso de diccionarios y condicionales
  - bucles (`for` y `while`)
  - funciones (básicas, docstrings, parámetros por defecto)
  - funciones lambda

- `python/clase-python3/clase3.py`: tercera clase de Python. Se trabajan:
  - entrada de datos con `input()`
  - casting (conversión de tipos)
  - redondeo con `round()`
  - control de bucles con `break` y `continue`
  - manejo de errores con `try`, `except` y `finally`
  - módulos propios (`python/clase-python3/modules/`: `mates.py` y `saludos.py`)

- `git/clase-git/`: carpeta creada principalmente como ejercicio de Git. En ella hay varios archivos y scripts sencillos, pero su objetivo real era practicar:
  - ramas
  - commits
  - merges
  - pull requests
  - resolución de conflictos
  - flujo de trabajo colaborativo

- `github-actions/`: cuarta clase, dedicada a GitHub Actions. Contiene los apuntes (`info-clase.md`) y un script de ejemplo (`escaneo_seguridad.py`). Los workflows están en `.github/workflows/` (GitHub solo detecta los que están directamente en esa carpeta) y sus archivos de datos JSON en `.github/workflows/data/`. Se trabajan:
  - estructura de un workflow (`on`, `jobs`, `runs-on`, `steps`)
  - triggers manuales con `workflow_dispatch` e `inputs`
  - uso de acciones (`uses`) como `actions/checkout`
  - variables de entorno (`env`), secretos (`secrets`) y variables del repo (`vars`)
  - matrices de estrategia (`strategy.matrix`)
  - dependencias entre jobs (`needs`) y condicionales (`if`)
  - outputs entre steps y entre jobs (`$GITHUB_OUTPUT`)
  - artefactos (`upload-artifact` / `download-artifact`)
  - filtros de rama y ruta en `push`
  - programación con `cron`
  - contenedores de servicio (Postgres)
  - validación de JSON con una acción de la comunidad
  - un desafío final (`20.desafio_final.yaml`) que integra todo lo anterior

- `docker/`: clases de Docker, cada una con un `README.md` que explica la presentación correspondiente:
  - [`clase-docker1`](docker/clase-docker1/README.md): kernel, máquinas virtuales, contenedores, Dockerfile, imágenes y primeros comandos.
  - [`clase-docker2`](docker/clase-docker2/README.md): `requirements.txt`, bind mounts, `ENTRYPOINT`/`CMD`, entorno Linux, puertos con Nginx e inspección de errores. Incluye `precios.py` y `test_precios.py`, junto con su propio `Dockerfile` y `requirements.txt` (`pytest` y `hypothesis`) para ejecutar los tests.
  - [`clase-docker3`](docker/clase-docker3/README.md): Docker Compose, volúmenes y PostgreSQL + pgAdmin.

- `sql/`: clases de SQL.
  - [`clase-sql1`](sql/clase-sql1/README.md): `CREATE TABLE`, `ALTER TABLE`, `INSERT`, `SELECT` con `WHERE`, `ORDER BY`, `LIMIT`, funciones, `GROUP BY`/`HAVING`, `UPDATE` y `DELETE` sobre la tabla `peliculas`.
  - [`clase-sql2`](sql/clase-sql2/README.md): relaciones entre tablas (primary key, foreign key; 1:1, 1:N y N:M), diseño y diagramas con dbdiagram.io, `REFERENCES` y `INNER`/`LEFT`/`RIGHT`/`FULL OUTER JOIN` con `IS NULL`, varias tablas y `GROUP BY`.
  - [`clase-sql3`](sql/clase-sql3/README.md): entregable (`Entregable.sql`) sobre `departamentos`, `empleados` y `proyectos`: tablas relacionadas, comparación de `INNER`/`LEFT`/`RIGHT`/`FULL OUTER JOIN` y subconsultas en el `WHERE` (`AVG`, `MAX`, búsqueda de un `id`).
  - [`sql-reto-final`](sql/sql-reto-final/README.md): reto final. PostgreSQL y una aplicación Python (`main.py`, con `psycopg`) en contenedores con Docker Compose; consulta la tabla `videojuegos` y la imprime. Incluye `consultas.sql`, `requirements.txt`, `.env.example`, `.dockerignore` y `.gitignore`; el `Dockerfile` y el `docker-compose.yml` solo se explican en su README, no están en el repositorio.

## Objetivos de aprendizaje

Este proyecto busca practicar:

- fundamentos de Python
- manejo de tipos de datos
- uso de estructuras como listas, diccionarios y tuplas
- uso de condicionales y operadores
- bucles, sets y funciones (incluidas las lambda)
- lectura de datos del usuario, casting y redondeo
- control de flujo en bucles (`break`, `continue`)
- gestión de errores con `try` / `except` / `finally`
- organización del código en módulos
- escritura de tests automáticos
- escritura de funciones simples
- entrada y salida por consola
- lógica de programación básica
- trabajo con Git y GitHub en equipo
- automatización con GitHub Actions: workflows, jobs, matrices, artefactos, outputs, secretos y servicios
- contenedores con Docker: imágenes, Dockerfile, volúmenes y Docker Compose
- conexión de una aplicación Python a PostgreSQL
- SQL en PostgreSQL: tablas, consultas, agregados, relaciones con claves foráneas, `JOIN` y subconsultas

## Requisitos

Necesitas tener instalado:

- Python 3
- Git
- Docker y Docker Compose (para las clases de `docker/` y el reto final de `sql/`)
- Un cliente de PostgreSQL para las clases de SQL: pgAdmin (de [clase-docker3](docker/clase-docker3/README.md)) o la extensión PostgreSQL de VS Code

## Cómo ejecutarlo

Para ejecutar los scripts de la carpeta de Git:

```bash
cd git/clase-git
python3 app.py
python3 interes-compuesto.py
python3 numeros-aleatorios.py
```

Para ejecutar el ejemplo introductorio de Python:

```bash
cd python/clase-python1
python3 clase1.py
```

Para ejecutar la segunda clase de Python:

```bash
cd python/clase-python2
python3 clase2.py
```

Para ejecutar la tercera clase de Python:

```bash
cd python/clase-python3
python3 clase3.py
```

Para los tests de la clase Docker 2:

```bash
cd docker/clase-docker2
docker build -t mis-tests .
docker run --rm mis-tests
```

Para la clase de GitHub Actions, los workflows se lanzan desde la pestaña **Actions** del repositorio (**Run workflow**). El script de ejemplo se puede probar en local:

```bash
python3 github-actions/escaneo_seguridad.py .github/workflows/data/ventas.json
```

Para el desafío final hay que crear antes el secreto `DISCORD_WEBHOOK` en Settings → Secrets and variables → Actions.

Para el reto final de SQL (requiere el `docker-compose.yml` y el `Dockerfile` del proyecto local, ver [su README](sql/sql-reto-final/README.md)):

```bash
cd sql/sql-reto-final
cp .env.example .env          # y edita la contraseña
docker compose up -d db
# ejecuta consultas.sql sobre pruebadb (ver README del reto)
docker compose up --build app
```

## Nota importante

La carpeta `git/clase-git` no es un proyecto funcional complejo ni un producto final. Fue principalmente una práctica para aprender a trabajar con Git, ramas, merges y pull requests. La parte más importante de ese ejercicio era el proceso de colaboración y manejo del repositorio, no la lógica del programa en sí.

## Estado del proyecto

Proyecto de aprendizaje en curso: se va ampliando con cada clase del máster (Python, Git y GitHub Actions, Docker, SQL (junto con el reto final de SQL)).
