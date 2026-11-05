# Clases de APIs con FastAPI

Apuntes y ejercicios de las clases de APIs: qué es una API, cómo construir una con FastAPI, cómo conectarla a una base de datos MySQL y cómo protegerla con distintos tipos de autenticación.

## Estructura

```text
apis/
├── clase1/
│   ├── ejercicio2.md      # Introducción a las APIs (teoría + prueba real)
│   ├── ejercicio3.py      # Primera app FastAPI: 5 endpoints
│   └── ejercicio6.py      # API de notas con paginación (offset y cursor)
└── clase2/
    ├── 06b-mysql-database/  # API sobre una base de datos MySQL (Library API)
    ├── 08-basic-auth/       # Autenticación Basic Auth
    ├── 09-api-key-auth/     # Autenticación con API key
    ├── 10-public-api/       # Consumo de una API pública (OpenWeatherMap) + JWT
    └── 11-jwt-auth/         # Autenticación con JSON Web Tokens
```

Cada ejercicio de `clase2/` tiene su propio `readme*.md` (en inglés) con el enunciado completo.

## Clase 1

### Ejercicio 2: introducción a las APIs ([`ejercicio2.md`](clase1/ejercicio2.md))
- Qué es una API y cómo funciona en una aplicación web (petición HTTP, endpoint, método, código de estado y JSON).
- Por qué son importantes: reutilización, integración, separación de responsabilidades y escalabilidad.
- Cuatro APIs populares (GitHub, Google Maps, Stripe y PokéAPI) y una prueba real con PokéAPI.

### Ejercicio 3: primera app FastAPI ([`ejercicio3.py`](clase1/ejercicio3.py))
Cinco endpoints: `GET /`, `GET /about`, `GET /api/hello`, `GET /api/user/{username}` y `POST /api/greet`. Se trabajan:
- instalación de FastAPI y servidor de desarrollo (`fastapi dev`)
- *path operations*, métodos HTTP y parámetros de ruta
- respuestas JSON y de texto plano (`PlainTextResponse`)
- cuerpo JSON validado con un modelo de Pydantic (`BaseModel`)
- documentación automática en `/docs` y pruebas con Postman

### Ejercicio 6: API de notas con paginación ([`ejercicio6.py`](clase1/ejercicio6.py))
CRUD en memoria de notas (`/notes`) con 95 notas de ejemplo. Se trabajan:
- `POST` (201 + cabecera `Location`), `GET`, `PUT`, `PATCH` y `DELETE` (204)
- paginación por **offset** (`?offset=&limit=`) y por **cursor** opaco en base64 (`?cursor=&limit=`), con enlaces `next`/`prev` y cabecera `Link` (RFC 8288)
- validación de parámetros (`limit` entre 1 y 100: fuera de rango es 422, no se recorta)
- errores en formato *problem details* (RFC 9457)

## Clase 2

| Ejercicio | Tema | Qué se trabaja |
|---|---|---|
| [`06b-mysql-database`](clase2/06b-mysql-database/readme06b.md) | API sobre MySQL | Conexión con PyMySQL, SQL con parámetros (`%s`), `JOIN`, `LIMIT`/`OFFSET`, transacciones (`commit`/`rollback`), errores de integridad traducidos a `409`/`422`, filtros `?author_id=` y `?q=` |
| [`08-basic-auth`](clase2/08-basic-auth/readme08.md) | Basic Auth | `HTTPBasic`, contraseñas con `bcrypt`, cabecera `WWW-Authenticate`, comprobación en tiempo constante |
| [`09-api-key-auth`](clase2/09-api-key-auth/readme09.md) | API key | Cabecera `X-API-Key`, claves aleatorias (`secrets`), guardar solo el hash SHA-256, mostrarla una vez, rotar y revocar |
| [`10-public-api`](clase2/10-public-api/readme10.md) | API pública | Consumir OpenWeatherMap con `httpx` (geocodificación + tiempo), timeouts, errores `502`/`503`, claves en `.env`, login con JWT |
| [`11-jwt-auth`](clase2/11-jwt-auth/readme11.md) | JWT | Access y refresh tokens, claims `exp`/`iss`/`aud`/`jti`/`type`, `/refresh`, `/logout` con revocación por `jti` |

## Cómo ejecutarlo

Requisitos: **Python 3.10 o superior** (con el 3.9 que trae macOS falla por la sintaxis `str | None`). Se usa **un único entorno virtual para todo el repositorio**, el de la raíz (`.venv`):

```bash
# Desde la raíz del repositorio (solo la primera vez)
python3 -m venv .venv            # usa un Python 3.10+ (por ejemplo, el de Homebrew)
source .venv/bin/activate
pip install "fastapi[standard]" bcrypt PyJWT httpx python-dotenv PyMySQL cryptography
```

Después, en cada ejercicio:

```bash
source .venv/bin/activate        # desde la raíz
cd apis/clase2/08-basic-auth     # o cualquier otra carpeta
fastapi dev app.py
```

Abre http://127.0.0.1:8000/docs para probar los endpoints (el botón **Authorize** sirve para meter usuario, clave o token).

### Notas por ejercicio

- **`clase1/ejercicio3.py` y `ejercicio6.py`**: `fastapi dev ejercicio3.py` (o `ejercicio6.py`) desde `apis/clase1`.
- **`06b-mysql-database`**: necesita MySQL en Docker. Desde su carpeta:

  ```bash
  cp .env.example .env
  docker compose up -d --wait      # arranca MySQL (y Adminer)
  fastapi dev app.py
  docker compose down              # al terminar (conserva los datos; `-v` los borra)
  ```

- **`10-public-api`**: `/weather` necesita una clave gratuita de [OpenWeatherMap](https://openweathermap.org/api) en su `.env`:

  ```bash
  cp .env.example .env             # y rellena OPENWEATHER_API_KEY=
  ```

  Las claves nuevas pueden tardar hasta 2 horas en activarse (mientras tanto, `/weather` responde 503).
- **`11-jwt-auth` y `10-public-api`**: `JWT_SECRET_KEY` es opcional. Si está vacía se genera una al arrancar y los tokens dejan de valer al reiniciar.
- Los ficheros `.env` están en el `.gitignore`: **nunca se suben** (contienen claves).
- Los usuarios, claves y notas de los ejercicios se guardan **en memoria** y se pierden al reiniciar la app (salvo los libros de `06b`, que están en MySQL).
