# Reto final SQL 3 — PostgreSQL + Python + Docker

Proyecto en dos fases: una base de datos PostgreSQL levantada con Docker Compose y una aplicación en Python (en otro contenedor) que consulta esa misma base de datos y muestra por terminal los registros de la tabla `videojuegos`.

## Estructura del proyecto que se creó en local

```
.
├── README.md
├── docker-compose.yml   # servicios db (PostgreSQL) y app (Python)
├── Dockerfile           # imagen de la aplicación Python
├── .dockerignore        # evita copiar .env y .git a la imagen
├── .gitignore           # evita subir .env a GitHub
├── .env.example         # plantilla de variables de entorno
├── requirements.txt     # dependencias de Python (psycopg)
├── main.py              # conecta a la BD y hace el SELECT
└── consultas.sql        # CREATE TABLE, INSERT y SELECT
```

## Configuración

1. Copia la plantilla de variables de entorno:

   ```bash
   cp .env.example .env
   ```

2. Edita `.env` y sustituye `cambia_esta_contrasena` por tu contraseña. Debe coincidir en `POSTGRES_PASSWORD` y en `DATABASE_URL`.

| Variable | Descripción |
|---|---|
| `POSTGRES_USER` | Usuario de PostgreSQL |
| `POSTGRES_PASSWORD` | Contraseña de PostgreSQL |
| `POSTGRES_DB` | Base de datos que se crea al inicializar (`pruebadb`) |
| `DATABASE_URL` | Cadena de conexión que usa Python dentro de Docker (host `db`, puerto interno `5432`) |

> `.env` contiene credenciales y **no** se sube a GitHub (está en `.gitignore`).

## Fase 1 — PostgreSQL

Arranca la base de datos en segundo plano y comprueba que está activa:

```bash
docker compose up -d db
docker compose ps
docker compose logs db   # si algo falla
```

### Conexión desde VS Code

En la extensión PostgreSQL: *Add Connection* → *Connection String*:

```
postgresql://postgres@127.0.0.1:5433/pruebadb
```

Introduce la contraseña de tu `.env`. Se usa `127.0.0.1:5433` porque VS Code corre en tu ordenador y entra por el puerto publicado; `db:5432` solo es válido dentro de la red de Docker.

### Tabla y datos

El contenido de [consultas.sql](consultas.sql) se ejecuta desde la extensión sobre `pruebadb`. Crea la tabla `videojuegos` e inserta tres registros:

| Columna | Tipo | Restricción |
|---|---|---|
| `id` | `SERIAL` | `PRIMARY KEY` |
| `titulo` | `TEXT` | `NOT NULL` |
| `plataforma` | `VARCHAR(50)` | |
| `anio` | `INTEGER` | |

También puede ejecutarse desde la terminal:

```bash
docker compose exec -T db sh -c 'psql -U $POSTGRES_USER -d $POSTGRES_DB' < consultas.sql
```

## Fase 2 — Aplicación Python

- [requirements.txt](requirements.txt): `psycopg[binary]==3.1.18`.
- [Dockerfile](Dockerfile): parte de `python:3.11-slim`, instala dependencias, copia el código y ejecuta `main.py`.
- [main.py](main.py): lee `DATABASE_URL` del entorno, se conecta con `psycopg`, ejecuta `SELECT * FROM videojuegos;` e imprime cada fila.
- El servicio `app` de `docker-compose.yml` se construye con `build: .`, recibe `.env` y depende de `db`.

### Cómo funciona `main.py`

```python
import os
import psycopg

url = os.getenv("DATABASE_URL")

try:
    with psycopg.connect(url) as connection:
        with connection.cursor() as cur:
            cur.execute("SELECT * FROM videojuegos;")
            filas = cur.fetchall()

            for fila in filas:
                print(fila)
except Exception as e:
    print("Error:", e)
    raise
```

El script hace, de arriba abajo:

1. **Lee la cadena de conexión.** `os.getenv("DATABASE_URL")` toma la variable de entorno que Docker Compose inyecta desde `.env`. La contraseña no está escrita en el código. Si la variable no existe devuelve `None` y `psycopg.connect` fallará.
2. **Abre la conexión.** `psycopg.connect(url)` se conecta a PostgreSQL. Dentro de Docker el host es `db` (el nombre del servicio en `docker-compose.yml`) y el puerto el interno `5432`, no el `5433` que se publica hacia tu ordenador.
3. **Crea un cursor.** El cursor (`connection.cursor()`) es el objeto que envía sentencias SQL y recoge sus resultados.
4. **Ejecuta la consulta.** `cur.execute("SELECT * FROM videojuegos;")` lanza el `SELECT` sobre la tabla creada con `consultas.sql`.
5. **Recoge las filas.** `cur.fetchall()` devuelve todas las filas como una lista de tuplas, una por registro, con las columnas en el orden de la tabla: `(id, titulo, plataforma, anio)`.
6. **Las imprime.** El bucle `for` muestra cada tupla por la salida estándar, que es lo que se ve en `docker compose up app` y en `docker compose logs app`.
7. **Gestiona errores.** El `try/except` imprime `Error: <mensaje>` (por ejemplo, `connection refused` o `relation "videojuegos" does not exist`) y `raise` vuelve a lanzar la excepción, de modo que el proceso termina con error y el contenedor sale con un código distinto de 0 en vez de fallar en silencio.

Detalles sobre los `with`:

- `with psycopg.connect(...)` cierra la conexión automáticamente al salir del bloque. Además, si el bloque termina bien confirma (`commit`) la transacción abierta y, si hay excepción, la revierte (`rollback`). Aquí solo se lee, así que no cambia nada, pero es el patrón correcto cuando se hacen `INSERT`, `UPDATE` o `DELETE`.
- `with connection.cursor()` cierra el cursor al terminar.

Cosas a tener en cuenta:

- El script **solo lee**: no crea la tabla ni inserta datos. Antes hay que ejecutar `consultas.sql` (Fase 1); si no, falla con `relation "videojuegos" does not exist`.
- Ejecuta una sola vez y termina; no queda en marcha como un servidor. Por eso `docker compose ps` no lo muestra activo tras imprimir.
- `SELECT *` devuelve tuplas posicionales. Para elegir columnas se escribiría, por ejemplo, `SELECT titulo, anio FROM videojuegos;`, y para filtrar se usarían parámetros (`cur.execute("... WHERE anio = %s", (2017,))`) en lugar de concatenar texto, para evitar inyección SQL.
- `depends_on: db` solo asegura que el contenedor de la base arranca antes, no que PostgreSQL ya acepte conexiones; si la app arranca demasiado pronto puede dar `connection refused` (ver [solución de problemas](#solución-de-problemas)).

Ejecútala (con `db` ya en marcha):

```bash
docker compose up --build app
```

Salida esperada:

```
app-1  | (1, 'The Legend of Zelda: Breath of the Wild', 'Switch', 2017)
app-1  | (2, 'Hollow Knight', 'PC', 2017)
app-1  | (3, 'God of War', 'PS4', 2018)
```

## Comandos útiles

```bash
docker compose down        # para los contenedores (conserva los datos)
docker compose down -v     # para y BORRA el volumen con los datos
docker compose logs app    # logs de la aplicación
```

## Solución de problemas

| Problema | Qué revisar |
|---|---|
| `connection refused` | Que `db` esté iniciado y PostgreSQL haya terminado de arrancar. |
| `relation "videojuegos" does not exist` | Que ejecutaste `consultas.sql` sobre `pruebadb`. |
| `database "pruebadb" does not exist` | El volumen se inicializó antes con otro `POSTGRES_DB`. Créala con `docker compose exec db psql -U postgres -c 'CREATE DATABASE pruebadb;'`. |
| No aparecen los cambios de Python | Reconstruye con `docker compose up --build app`. |
| VS Code no conecta | Puerto (`5433`), usuario, contraseña y base de datos. |
| Python no conecta dentro de Docker | `DATABASE_URL` debe usar `db:5432`, no `localhost:5433`. |
| Cambié la contraseña en `.env` y no surte efecto | El volumen conserva la base ya inicializada; `POSTGRES_PASSWORD` solo se aplica la primera vez. |
