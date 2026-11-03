# Repositorio de clases de Máster de IA, Data & Cloud @ EDEM Escuela de Empresarios

Este repositorio reúne los ejercicios y apuntes de las clases del máster: Python, Git y GitHub Actions, Docker, SQL con PostgreSQL y Data Science con NumPy y pandas, además de un reto final que integra SQL, Python y Docker. No se trata de un proyecto de producción, sino de un espacio para practicar y documentar cada clase (casi todas tienen su propio `README.md`).

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

- `git/`: clases de Git y GitHub, con sus apuntes en [`git/README.md`](git/README.md). Contiene varios archivos y scripts sencillos (`app.py`, `interes-compuesto.py`, `numeros-aleatorios.py`, `fichero.txt`, `documento-main.txt`), pero su objetivo real era practicar el flujo de trabajo. Se trabajan:
  - ramas, commits, merges y resolución de conflictos
  - pull requests y flujo de trabajo colaborativo
  - Git por línea de comandos (`init`, `clone`, `add`, `commit`, `push`, `pull`, `fetch`, `log`, `diff`, `restore`, `revert`, `switch`, `merge`, `remote`)
  - fork y remoto `upstream`
  - reglas de protección de ramas (*branch protection rules*): PR obligatoria, aprobaciones, checks, bloqueo de force push
  - `CODEOWNERS`: revisores obligatorios por fichero o carpeta
  - plantilla de pull request (`PULL_REQUEST_TEMPLATE.md`)
  - `.gitignore`

- `.github/`: configuración de GitHub del repositorio:
  - `CODEOWNERS`: propietarios del código (hoy, `/README.md` pertenece a `@Fisjo`)
  - `PULL_REQUEST_TEMPLATE.md`: texto precargado en cada nueva pull request
  - `workflows/`: workflows de GitHub Actions (ver `github-actions/` más abajo)

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

- `data-science/clase1/numpy.ipynb`: primera clase de Data Science, un notebook de Jupyter sobre NumPy. Cada celda de código tiene encima una celda de markdown que la explica, y termina con retos prácticos (simular las bicis disponibles en una red de estaciones, temperaturas, etc.). Se trabajan las siguientes funciones, métodos y atributos de NumPy:
  - **Importación y versión:** `import numpy as np`, `np.__version__`
  - **Atributos de un array:** `shape`, `ndim`, `size`, `dtype`
  - **Crear arrays:** `np.array()`, `np.zeros()`, `np.ones()`, `np.arange()`, `np.linspace()`
  - **Tipos y conversión:** `astype()`, `np.round()`
  - **Cambiar la forma:** `reshape()` (incluido `-1` para calcular una dimensión automáticamente)
  - **Números aleatorios:** `np.random.default_rng()` (con semilla), `integers()`, `random()`, `poisson()`
  - **Indexado y slicing:** índices, `[fila, columna]`, `[:, col]`, `[::-1]` y listas de índices
  - **Copias:** `copy()`
  - **Máscaras booleanas y condiciones:** comparaciones, `&`, `sum()`, `mean()`
  - **Posiciones y condicionales:** `np.argwhere()`, `np.where()`
  - **Ordenar:** `np.sort()`
  - **Operaciones entre arrays:** suma, resta y multiplicación elemento a elemento, `np.cumsum()`, `np.cumprod()`, `np.diff()`, `np.clip()`
  - **Comprobaciones:** `np.array_equal()`

- `data-science/clase2/pandas.ipynb`: segunda clase de Data Science, un notebook de Jupyter sobre pandas, con el mismo formato (una celda de markdown explicativa sobre cada celda de código). Usa los datos de `data-science/clase2/data/` (`stations.csv`, `usage_hourly.csv` y `weather_daily.json`, entre otros) sobre una red de bicis compartidas. Se trabajan las siguientes funciones y métodos de pandas:
  - **Estructuras:** `pd.Series()`, `pd.DataFrame()`, `columns`, `dtypes`
  - **Cargar datos:** `pd.read_csv()`, `pd.read_json()`
  - **Explorar:** `head()`, `describe()`, `isna()`, `duplicated()`, `nunique()`, `value_counts()`
  - **Columnas nuevas:** asignación directa, `round()`, `np.where()`
  - **Seleccionar y filtrar:** `loc`, `iloc`, `query()`, máscaras booleanas con `&`, `str.contains()`
  - **Ordenar:** `sort_values()` (varias columnas y orden por columna), `tolist()`
  - **Limpieza:** `copy()`, `drop_duplicates()`, `between()`, `reset_index()`
  - **Fechas:** `pd.to_datetime()`, accesor `.dt` (`date`, `hour`, `day_name()`, `dayofweek`)
  - **Agrupar y rellenar nulos:** `groupby()`, `ffill()`, `bfill()`, `fillna()`, `transform()`, `median()`
  - **Texto:** `str.strip()`, `str.lower()`, `str.title()`
  - **Retos:** valores imposibles, estaciones grandes del centro, ranking de lecturas, limpieza de duplicados, fechas, nulos y distritos

- `data-science/clase3/mathplot-seaborn.ipynb`: tercera clase de Data Science, un notebook de Jupyter sobre visualización con Matplotlib y Seaborn. Reutiliza los datos de la red de bicis de `data-science/clase2/data/` (`stations.csv`, `stations_clean.csv`, `usage_hourly.csv`, `weather_daily.json` y `rentals_by_hour.csv`), con rutas relativas `../clase2/data/...`. Empieza con una limpieza (duplicados, valor centinela `999` como dato ausente, `merge` con las estaciones, columnas de hora y día de la semana) y continúa con retos y análisis exploratorios. Se trabajan:
  - **Importación:** `matplotlib.pyplot as plt`, `seaborn as sns`
  - **Figuras y ejes:** `plt.subplots()` (una figura o una cuadrícula), `figsize`, `tight_layout()`, `plt.show()`
  - **Gráficos con Matplotlib:** líneas (`plot`), barras (`bar`, `barh`, `plot(kind="bar")`), histogramas (`hist`), dispersión (`scatter`), `fill_between()`, `axhline()`, `axvline()`, `axvspan()`, `annotate()`
  - **Personalización:** títulos, etiquetas de ejes, leyendas, rejilla, colores, formato de fechas (`DateFormatter`, `DayLocator`) y etiquetas sobre las barras (`bar_label`)
  - **Gráficos con Seaborn:** `histplot()`, `boxplot()`, `stripplot()` y `heatmap()`
  - **Preparación de datos para graficar:** `groupby()`, `pivot_table()`, `unstack()`, `merge()`, `pd.cut()`, `idxmax()` / `idxmin()`
  - **Retos:** el mes día a día, media por día de la semana, cuatro gráficos en una figura, perfil horario por distrito en fin de semana, bicis disponibles en laborables frente a fines de semana y mapa de calor día x hora
  - **Análisis exploratorio (EDA):** cuántos alquileres menos hay en fin de semana, qué distritos se vacían por la mañana y cuánto baja el uso con lluvia

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
- Git por línea de comandos: commits, ramas, merges, conflictos y deshacer cambios
- colaboración en GitHub: pull requests, forks, reglas de protección de ramas, `CODEOWNERS` y plantillas de PR
- automatización con GitHub Actions: workflows, jobs, matrices, artefactos, outputs, secretos y servicios
- contenedores con Docker: imágenes, Dockerfile, volúmenes y Docker Compose
- conexión de una aplicación Python a PostgreSQL
- SQL en PostgreSQL: tablas, consultas, agregados, relaciones con claves foráneas, `JOIN` y subconsultas
- análisis de datos con NumPy: arrays, indexado, máscaras booleanas, números aleatorios y operaciones vectorizadas
- análisis de datos con pandas: `DataFrame`, filtrado, limpieza, fechas, agrupaciones y tratamiento de nulos
- visualización de datos con Matplotlib y Seaborn: gráficos de líneas, barras, histogramas, dispersión y mapas de calor, y análisis exploratorio (EDA)

## Requisitos

Necesitas tener instalado:

- Python 3
- Git
- Docker y Docker Compose (para las clases de `docker/` y el reto final de `sql/`)
- Para los notebooks de `data-science/`: Jupyter (o VS Code con la extensión Jupyter) y NumPy, pandas, Matplotlib y Seaborn (`pip install numpy pandas matplotlib seaborn ipykernel`)
- Un cliente de PostgreSQL para las clases de SQL: pgAdmin (de [clase-docker3](docker/clase-docker3/README.md)) o la extensión PostgreSQL de VS Code

## Cómo ejecutarlo

Para ejecutar los scripts de la carpeta de Git:

```bash
cd git
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

Para los notebooks de Data Science, ábrelos en VS Code o Jupyter, elige un kernel de Python con NumPy, pandas, Matplotlib y Seaborn instalados y ejecuta las celdas en orden. El notebook de pandas carga los datos con rutas relativas (`./data/...`) y el de visualización con `../clase2/data/...`, así que cada uno debe ejecutarse desde su carpeta:

```bash
pip install numpy pandas matplotlib seaborn ipykernel
jupyter notebook data-science/clase1/numpy.ipynb
jupyter notebook data-science/clase2/pandas.ipynb
jupyter notebook data-science/clase3/mathplot-seaborn.ipynb
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

La carpeta `git/` no es un proyecto funcional complejo ni un producto final. Fue principalmente una práctica para aprender a trabajar con Git, ramas, merges, pull requests, forks y reglas de protección. La parte más importante de ese ejercicio era el proceso de colaboración y manejo del repositorio, no la lógica del programa en sí.

## Estado del proyecto

Proyecto de aprendizaje en curso: se va ampliando con cada clase del máster (Python, Git y GitHub Actions, Docker, SQL (junto con el reto final de SQL) y Data Science con NumPy, pandas y visualización con Matplotlib y Seaborn).
