# Clase Docker 3 · Docker Compose y volúmenes

Explicación organizada de la presentación **Docker 3** (Máster en Desarrollo Web, IA aplicada y DevOps · EDEM, Sofía Pinilla y Javier Plaza). Esta clase pasa de `docker run` con comandos largos a **Docker Compose**, introduce los **volúmenes** y termina dejando listo **PostgreSQL + pgAdmin** para la clase de SQL. No hay código en la carpeta; los ejemplos están en esta guía.

## Objetivos

1. Repasar el Dockerfile con `requirements.txt`.
2. Entender qué es Docker Compose y escribir un `compose.yaml`.
3. Manejar `up`, `ps`, `logs` y `down`.
4. Guardar datos en un volumen para que no se pierdan.
5. Dejar preparado PostgreSQL y pgAdmin.

## Índice

1. [Repaso del Dockerfile con requirements](#1-repaso-del-dockerfile-con-requirements)
2. [¿Qué es Docker Compose?](#2-qué-es-docker-compose)
3. [YAML en dos minutos](#3-yaml-en-dos-minutos)
4. [Nuestro primer compose.yaml](#4-nuestro-primer-composeyaml)
5. [Compose con dependencias](#5-compose-con-dependencias)
6. [Comandos de Docker Compose](#6-comandos-de-docker-compose)
7. [Una base de datos con Compose](#7-una-base-de-datos-con-compose)
8. [Volúmenes](#8-volúmenes)
9. [PostgreSQL + pgAdmin](#9-postgresql--pgadmin)
10. [Práctica final: el archivo .env](#10-práctica-final-el-archivo-env)
11. [Chuleta, errores frecuentes y repaso](#11-chuleta-errores-frecuentes-y-repaso)
12. [Prácticas y retos](#12-prácticas-y-retos)

---

## 1. Repaso del Dockerfile con requirements

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["pytest"]
```

- `requirements.txt` lista las librerías, una por línea. Solo el nombre instala la última versión estable; con `==` (`pytest==8.3.4`) se fija una versión exacta.
- Si añades una librería nueva, hay que **reconstruir la imagen** (`docker build`).
- `RUN` se ejecuta al construir; `CMD`, al arrancar. Se copia `requirements.txt` antes que el resto para aprovechar la caché de capas.

Opciones de `docker run` ya conocidas:

| Opción | Para qué sirve |
|---|---|
| `-d` | Segundo plano |
| `--name mi-app` | Nombre del contenedor |
| `-p 8080:80` | Publicar puerto: tu ordenador : contenedor |
| `-v .:/app` | Bind mount: tu carpeta : carpeta del contenedor |

Test de calentamiento (respuestas): `RUN pip install` se ejecuta **al construir la imagen**; con `-p 3000:80` se abre `http://localhost:3000`; con bind mount basta **volver a ejecutar `docker run`** tras cambiar el código.

## 2. ¿Qué es Docker Compose?

El problema: los comandos se hacen largos y hay que recordarlos y escribirlos igual cada vez, para cada contenedor y cada persona del equipo:

```bash
docker run -d --name mi-app -p 8080:80 -v .:/app mi-app
docker run -d --name mi-db  -p 5432:5432 -v datos:/datos mi-db
```

**Docker Compose** lee un archivo, `compose.yaml`, y con él crea, configura y arranca los contenedores: todo lo del `docker run`, escrito en un archivo.

- Arrancas **varios contenedores con un solo comando**.
- El archivo se guarda con el proyecto: todo el equipo lo levanta igual.

## 3. YAML en dos minutos

Formato de configuración en texto:

```yaml
nombre: Sofía
curso:
  titulo: Docker 3
  alumnos: 22
temas:
  - compose
  - volúmenes
```

- `clave: valor`.
- **La sangría manda** (como en Python): dos espacios, **nunca tabuladores**.
- Un guion `-` es un elemento de una lista.

## 4. Nuestro primer compose.yaml

```yaml
services:
  app:
    image: python:3.11-slim
    working_dir: /app
    command: ["python", "main.py"]
    volumes:
      - .:/app
```

| Clave | Equivale a |
|---|---|
| `services` | Lista de contenedores; cada uno es un **servicio** |
| `app` | Nombre del servicio (lo eliges tú) |
| `image` | Imagen que usa |
| `working_dir` | `WORKDIR` |
| `command` | `CMD` |
| `volumes` | El bind mount de tu carpeta |

Se levanta, desde la carpeta del `compose.yaml`, con:

```bash
docker compose up
# app-1  | Hola desde Compose
# app-1 exited with code 0
```

Sin imagen, puertos ni rutas en el comando: todo lo lee del archivo.

## 5. Compose con dependencias

La imagen `python:3.11-slim` no trae `pytest`. Dos formas de resolverlo:

**a) Construir con el Dockerfile (recomendada)**

```yaml
services:
  app:
    build: .
```

`build: .` sustituye a `image:`: Compose construye la imagen con el Dockerfile de la carpeta; ya no hace falta `docker build` a mano. La primera vez `up` construye; tras cambiar código o dependencias:

```bash
docker compose up --build
```

**b) Instalar al arrancar (solo para probar rápido)**

```yaml
services:
  app:
    image: python:3.11-slim
    working_dir: /app
    command: >
      sh -c "pip install -r requirements.txt &&
             pytest"
    volumes:
      - .:/app
```

`sh -c "…"` ejecuta varios comandos y `&&` encadena (el siguiente solo si el anterior va bien). Inconveniente: **instala las librerías en cada arranque**; con `build` solo se instalan una vez.

Un **servicio** es cada uno de los contenedores que describe el archivo.

## 6. Comandos de Docker Compose

`up` crea y arranca todo lo que dice el archivo; `down` lo detiene **y lo elimina**. Todos se ejecutan en la carpeta del `compose.yaml`.

| Comando | Para qué sirve |
|---|---|
| `docker compose up` | Crear y arrancar los servicios viendo su salida |
| `docker compose up -d` | Lo mismo, en segundo plano |
| `docker compose ps` | Ver servicios y su estado |
| `docker compose logs` | Ver lo que han escrito los servicios |
| `docker compose logs postgres` | Ver la salida de un solo servicio |
| `docker compose up --build` | Reconstruir las imágenes y arrancar |
| `docker compose down` | Detener y eliminar los contenedores |

Orden lógico: `up -d` → `ps` → `logs` → `down`. (`stop` solo detiene; `down` además elimina.)

## 7. Una base de datos con Compose

**PostgreSQL** es una base de datos: un programa que guarda datos de forma ordenada y los entrega cuando otro programa se los pide. Como Nginx, **no termina**: se queda esperando peticiones, en el puerto **5432**. Hoy solo se pone en marcha; se usará en la clase de SQL.

```yaml
services:
  postgres:
    image: postgres:18.6-alpine
    environment:
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
```

- `environment`: **variables de entorno**, datos que el programa lee al arrancar. PostgreSQL exige una contraseña.
- `ports`: publica el 5432 para conectar desde tu ordenador.

```bash
docker compose up -d
docker compose ps
docker compose logs postgres
# database system is ready to accept connections
```

**Predicción:** si los datos se guardan dentro del contenedor y haces `down` + `up`, **se pierden**: lo de dentro de un contenedor muere con él.

## 8. Volúmenes

Un **volumen** es un espacio para datos **fuera del contenedor**, creado y guardado por Docker. Se «enchufa» a una carpeta del contenedor, como un USB. Si eliminas el contenedor, el volumen **sigue ahí** y el siguiente contenedor lo vuelve a enchufar. Resuelve el pendiente de Docker 1 («los datos no se guardan solos»).

```yaml
services:
  postgres:
    image: postgres:18.6-alpine
    environment:
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql
volumes:
  postgres_data:
```

- `postgres_data:/var/lib/postgresql` → nombre del volumen : carpeta del contenedor donde PostgreSQL guarda sus datos.
- El bloque `volumes:` final (sin sangría) declara que el volumen existe. El nombre lo eliges tú.

### Volumen vs bind mount

| | Bind mount | Volumen |
|---|---|---|
| Cómo se escribe | `- ./datos:/app/datos` | `- postgres_data:/var/lib/postgresql` |
| Cómo distinguirlos | Empieza por `.` o `/`: carpeta tuya | Solo un nombre: lo gestiona Docker |
| Dónde están los datos | En tu carpeta, a la vista | Guardados por Docker |
| Para qué | Programar: editas y ejecutas sin reconstruir | Datos que deben durar (bases de datos) |

### `down` no borra los volúmenes

```bash
docker compose down       # los datos siguen
docker volume ls          # lista los volúmenes
docker compose down -v    # ¡borra también los volúmenes: se pierden los datos!
```

Usa `-v` solo para empezar de cero. En la práctica 3, la segunda vez los logs dicen que ya existía una base de datos y se salta la creación; tras `down -v` PostgreSQL la crea desde cero.

## 9. PostgreSQL + pgAdmin

**pgAdmin** es una web para manejar bases PostgreSQL. Se añade como segundo servicio; dentro de Compose, **un servicio encuentra a otro por su nombre** (para pgAdmin, la base está en `postgres`).

```yaml
services:
  postgres:
    image: postgres:18.6-alpine
    # … lo de antes
  pgadmin:
    image: dpage/pgadmin4:9.17
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
```

pgAdmin escucha en el 80 del contenedor y se publica en el **5050** → `http://localhost:5050`. Un solo comando levanta los dos servicios.

## 10. Práctica final: el archivo .env

Las contraseñas no se escriben en el `compose.yaml` porque ese archivo se sube al repositorio. Van en un `.env` que se queda en tu ordenador; el repo trae una plantilla `.env.example` con valores de ejemplo, y Compose lee `.env` automáticamente.

```bash
git clone https://github.com/JaviPlazaRosique/postgresql_pgadmin.git
cd postgresql_pgadmin
cp .env.example .env
# seguir las instrucciones del repositorio
```

## 11. Chuleta, errores frecuentes y repaso

| Lo que ves | Causa | Solución |
|---|---|---|
| `no configuration file provided: not found` | No estás en la carpeta del `compose.yaml` | Ir a la carpeta del proyecto |
| `yaml: line 5: mapping values are not allowed…` | Sangría o dos puntos mal | Revisar la línea: espacios, no tabuladores |
| `…port is already allocated` | Puerto del ordenador ocupado | Cambiar el primer número o `down` del otro proyecto |
| `"pytest": executable file not found` | Falta `pytest` en `requirements.txt` o no reconstruiste | Añadirlo y `up --build` |

**Si puedes responder esto, lo has entendido:** qué problema resuelve Compose; qué es un servicio; qué hace `down` y qué `down -v`; en qué se diferencian volumen y bind mount.

## 12. Prácticas y retos

1. **Práctica 1 · primer compose.yaml:** `main.py` con `primera_letra(palabra)`, un `compose.yaml` con Python que lo ejecute y `docker compose up`. Cambiar la palabra y relanzar: no hay que reconstruir nada (bind mount).
2. **Práctica 2 · tests con Compose:** `test_main.py`, `requirements.txt` con pytest, Dockerfile con `CMD ["pytest"]` y `build: .` en el compose. Si cambias algo y quieres verlo, añade `--build`.
3. **Reto extra · contar letras:** `contar_letras(palabra)` devuelve un diccionario con las apariciones de cada letra (`"casa"` → `{"c": 1, "a": 2, "s": 1}`), con tests y todo dockerizado con Compose.
4. **Práctica 3 · base de datos que no pierde datos:** compose con `postgres` y el volumen `postgres_data`; `up -d`, `ps`, `logs`; `down` y volver a levantar; `docker volume ls`; `down -v` y levantar de nuevo, comparando los logs.
