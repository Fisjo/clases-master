# Reto final SQL 3 — PostgreSQL + Python + Docker

Proyecto en dos fases: una base de datos PostgreSQL levantada con Docker Compose y una aplicación en Python (en otro contenedor) que consulta esa misma base de datos y muestra por terminal los registros de la tabla `videojuegos`.

## Estructura del proyecto que se creó en local

```
.
├── README.md
├── docker-compose.yml   # servicios db (PostgreSQL) y app (Python)   [solo local, explicado abajo]
├── Dockerfile           # imagen de la aplicación Python            [solo local, explicado abajo]
├── .env                 # credenciales reales                        [solo local, no se sube]
├── .dockerignore        # evita copiar .env y .git a la imagen
├── .gitignore           # evita subir .env a GitHub
├── .env.example         # plantilla de variables de entorno
├── requirements.txt     # dependencias de Python (psycopg)
├── main.py              # conecta a la BD y hace el SELECT
└── consultas.sql        # CREATE TABLE, INSERT y SELECT
```

> En el repositorio solo están los archivos sin marca `[solo local…]`. `docker-compose.yml` y `Dockerfile` se explican en [Explicación de los archivos del proyecto](#explicación-de-los-archivos-del-proyecto) pero no se incluyen, así que **los comandos `docker compose` de este README solo funcionan en el proyecto local completo**, no clonando esta carpeta tal cual.

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

## Explicación de los archivos del proyecto

En esta carpeta se guardan [`consultas.sql`](consultas.sql), [`.env.example`](.env.example), [`main.py`](main.py), [`requirements.txt`](requirements.txt), [`.dockerignore`](.dockerignore) y [`.gitignore`](.gitignore). `docker-compose.yml` y `Dockerfile` se explican aquí pero **no se incluyen como archivos**, para que esta carpeta no sea por sí sola desplegable ni choque con el `Dockerfile` de la raíz del repositorio. El `.env` real tampoco se sube (contiene credenciales).

### `docker-compose.yml`

```yaml
services:
  db:
    image: postgres:17-alpine
    env_file: .env
    ports:
      - "5433:5432"
    volumes:
      - postgresDB:/var/lib/postgresql/data
    restart: unless-stopped

  app:
    build: .
    env_file: .env
    depends_on:
      - db

volumes:
  postgresDB:
```

Define **dos servicios** que Compose conecta en una misma red, donde cada uno es alcanzable por el nombre de su servicio:

| Línea | Qué hace |
|---|---|
| `image: postgres:17-alpine` | `db` usa la imagen oficial de PostgreSQL 17 sobre Alpine (ligera) |
| `env_file: .env` | Carga las variables del `.env` como entorno del contenedor. En `db`, la imagen usa `POSTGRES_USER`, `POSTGRES_PASSWORD` y `POSTGRES_DB` para crear el usuario y la base la primera vez |
| `ports: "5433:5432"` | Publica el puerto 5432 del contenedor como **5433** en tu ordenador (formato `host:contenedor`). Se usa 5433 para no chocar con un PostgreSQL local en el 5432. Es lo que usa VS Code |
| `volumes: postgresDB:/var/lib/postgresql/data` | Volumen con nombre donde PostgreSQL guarda los datos: sobreviven a `docker compose down` y solo se borran con `down -v` |
| `restart: unless-stopped` | Reinicia `db` si se cae o si arranca Docker, salvo que se haya parado a mano |
| `build: .` | `app` no usa una imagen publicada: se construye con el `Dockerfile` de esta carpeta |
| `depends_on: - db` | Arranca `db` antes que `app` (pero no espera a que PostgreSQL esté listo para aceptar conexiones) |
| `volumes: postgresDB:` (final) | Declara el volumen con nombre usado arriba |

`app` **no publica puertos**: solo se conecta hacia fuera, a `db:5432`, por la red interna.

### `Dockerfile`

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

| Instrucción | Qué hace |
|---|---|
| `FROM python:3.11-slim` | Imagen base: Python 3.11 en su variante reducida |
| `WORKDIR /app` | Directorio de trabajo dentro del contenedor |
| `COPY requirements.txt .` + `RUN pip install ...` | Copia e instala **solo las dependencias primero**: así Docker reutiliza esa capa en caché mientras `requirements.txt` no cambie |
| `COPY . .` | Copia el resto del código (aquí entra `main.py`). Por eso importa el `.dockerignore`: sin él también se copiaría el `.env` a la imagen |
| `CMD ["python", "main.py"]` | Comando que se ejecuta al arrancar el contenedor |

### `requirements.txt`

```
psycopg[binary]==3.1.18
```

- Lista las dependencias de Python que instala `pip install -r requirements.txt` en el `Dockerfile`.
- `psycopg` es el driver (versión 3) para hablar con PostgreSQL desde Python. El extra `[binary]` instala una versión precompilada, de modo que no hacen falta compiladores ni librerías de sistema (`libpq`) en la imagen `slim`.
- `==3.1.18` fija la versión exacta, para que la imagen se construya siempre igual.

### `.dockerignore`

```
.env
.git
__pycache__/
```

Indica qué **no** entra en la imagen cuando el `Dockerfile` ejecuta `COPY . .`:

- `.env`: evita que las credenciales queden **dentro de la imagen** (donde cualquiera con la imagen podría leerlas). La app las recibe en ejecución por `env_file` en `docker-compose.yml`, no desde la imagen.
- `.git`: el historial de Git no aporta nada al contenedor y lo haría más pesado.
- `__pycache__/`: bytecode de Python generado en local, innecesario.

### `.gitignore`

```
.env
__pycache__/
```

Indica qué **no** se sube a Git: `.env` (credenciales) y `__pycache__/` (archivos generados). Es el equivalente del `.dockerignore`, pero para el repositorio en vez de para la imagen: por eso se versiona `.env.example` y no `.env`. `.git` no aparece aquí porque Git ya ignora su propia carpeta.

### `.env` y `.env.example`

Archivo real (local, **no se sube a GitHub**):

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=pruebadb
DATABASE_URL=postgresql://postgres:postgres@db:5432/pruebadb
```

- Las tres primeras variables las lee la imagen de PostgreSQL para inicializarse.
- `DATABASE_URL` la lee `main.py`. Formato: `postgresql://usuario:contraseña@host:puerto/base`. El host es **`db`** (nombre del servicio) y el puerto el **interno `5432`**.
- `env_file` aplica el mismo `.env` a los dos servicios, así que `app` también recibe `POSTGRES_PASSWORD`, aunque solo use `DATABASE_URL`.
- La contraseña `postgres` vale para pruebas locales; en cualquier otro entorno debe cambiarse. [`.env.example`](.env.example) es la plantilla versionable: misma estructura, con `cambia_esta_contrasena` como marcador. La contraseña debe coincidir en `POSTGRES_PASSWORD` y `DATABASE_URL`.

### `consultas.sql`

Ver [`consultas.sql`](consultas.sql):

- `CREATE TABLE IF NOT EXISTS videojuegos`: crea la tabla si no existe. `id SERIAL PRIMARY KEY` es un entero autoincremental y clave primaria; `titulo` es obligatorio (`NOT NULL`); `plataforma` y `anio` admiten `NULL`.
- `INSERT INTO ... VALUES`: añade tres videojuegos (los ids 1, 2 y 3 los genera `SERIAL`).
- `SELECT * FROM videojuegos;`: muestra el resultado.
- **No es idempotente**: el `CREATE` tiene `IF NOT EXISTS`, pero el `INSERT` no. Ejecutarlo dos veces duplica los tres registros (con ids 4, 5 y 6). Para empezar de cero, `DROP TABLE videojuegos;` o `docker compose down -v`.
- PostgreSQL **no lo ejecuta solo**: hay que lanzarlo a mano (extensión de VS Code o `psql`, ver Fase 1).

### Cómo encajan las piezas

```
 tu ordenador                          red de Docker Compose
┌──────────────────────┐        ┌──────────────────────────────────┐
│ VS Code / psql       │ 5433 → │ db (postgres:17-alpine) :5432    │
└──────────────────────┘        │        ▲                         │
                                │        │ DATABASE_URL (db:5432)  │
                                │ app (python:3.11-slim)           │
                                │   └─ main.py → SELECT            │
                                └──────────────────────────────────┘
```

Orden de uso: `docker compose up -d db` → ejecutar `consultas.sql` → `docker compose up --build app` → `main.py` lee la tabla y la imprime.

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
