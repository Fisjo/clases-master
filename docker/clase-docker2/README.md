# Clase Docker 2 · Dependencias, bind mounts, Linux, puertos y errores

Explicación organizada de la presentación **Docker 2** (Máster en Desarrollo Web, IA aplicada y DevOps · EDEM, Sofía Pinilla). Continúa Docker 1 y profundiza en cómo se construyen imágenes con dependencias y cómo se gestionan los contenedores.

## Contenido de la carpeta

| Archivo | Descripción |
|---|---|
| `precios.py` | Función `precio_final(precio, descuento=0)` de la Práctica 1 |
| `test_precios.py` | Tests con `pytest` y `hypothesis` (ejemplos, propiedades y entradas inválidas) |
| `info-clase.md` | Apuntes sueltos de clase (Dockerfile, `docker build -t prueba .`, `docker run --rm --name -v`) |
| `Dockerfile` | Imagen que instala las dependencias y ejecuta `pytest` |
| `requirements.txt` | Dependencias: `pytest` y `hypothesis` |
| `README.md` | Esta guía |

El `Dockerfile` y el `requirements.txt` (`pytest`, `hypothesis`) están en esta misma carpeta y construyen la práctica. Los comandos se lanzan **desde esta carpeta** (`cd docker/clase-docker2`), porque el contexto del build (`.`) es esta carpeta y `pytest` descubre aquí los tests:

```bash
docker build -t mis-tests .
docker run --rm mis-tests                # ejecuta la copia que está en la imagen
docker run --rm -v .:/app mis-tests      # ejecuta tu carpeta actual (bind mount)
```

> Nota: `test_precios.py` incluye tests que esperan `ValueError` para descuentos fuera de 0–100 y precios negativos; `precios.py` aún no valida, así que esos tests fallan hasta que se añada esa validación.

## Objetivos

1. Instalar dependencias en la imagen con `requirements.txt` y dockerizar tests.
2. Usar **bind mounts** para probar cambios sin reconstruir.
3. Crear un **entorno Linux** en un contenedor y gestionar su ciclo de vida.
4. Entender **servidor web** y **puerto**, y publicar una web.
5. Averiguar por qué falla un contenedor con `docker ps -a` y `docker logs`.

## Índice

1. [Repaso de Docker 1](#1-repaso-de-docker-1)
2. [requirements.txt](#2-requirementstxt)
3. [Bind mounts](#3-bind-mounts)
4. [ENTRYPOINT y CMD](#4-entrypoint-y-cmd)
5. [Un entorno Linux en un contenedor](#5-un-entorno-linux-en-un-contenedor)
6. [Servidores web y puertos](#6-servidores-web-y-puertos)
7. [Inspección de errores](#7-inspección-de-errores)
8. [Chuleta y errores frecuentes](#8-chuleta-y-errores-frecuentes)

---

## 1. Repaso de Docker 1

**Dockerfile → imagen → contenedor:** la receta, el plato congelado y el plato servido. De una imagen salen muchos contenedores.

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
CMD ["python", "main.py"]
```

| Comando | Para qué sirve |
|---|---|
| `docker pull python:3.11-slim` | Descargar una imagen |
| `docker build -t mi-app .` | Construir imagen desde el Dockerfile |
| `docker images` | Ver imágenes |
| `docker run --name mi-contenedor mi-app` | Crear y arrancar un contenedor |
| `docker ps` / `docker ps -a` | Ver contenedores en ejecución / todos |

## 2. requirements.txt

Las librerías **no vienen en la imagen base**: Python sí, pero `pytest`, `pandas` o `flask` hay que instalarlos **al construir la imagen**. La lista va en `requirements.txt`, una librería por línea:

```text
numpy==1.26.4
pandas
pytest
```

Solo el nombre instala la última versión estable; `==` fija la versión exacta (lo que garantiza que todos ejecutan lo mismo: acuérdate de Andrea y Pablo).

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

- `--no-cache-dir`: pip no guarda instaladores; la imagen pesa menos.
- **RUN vs CMD:**

| | RUN | CMD |
|---|---|---|
| Cuándo | Al construir (`docker build`) | Al arrancar (`docker run`) |
| Para qué | Preparar el entorno (instalar librerías) | Poner en marcha la aplicación |
| Cuántos | Los que hagan falta | Solo cuenta el último |
| Cocina | Cocinar antes de congelar | Servir en la mesa |

### ¿Por qué copiar `requirements.txt` antes que el resto?

Docker guarda cada paso (capa) y lo reutiliza si no ha cambiado. El código cambia cada cinco minutos; las dependencias casi nunca. Si copias primero solo `requirements.txt`, retocar `main.py` reutiliza la capa lenta de `pip install` y solo repite `COPY . .` y `CMD`.

### Práctica 1 · dockerizar tests

Con `precios.py` y `test_precios.py` (esta carpeta), `requirements.txt` con `pytest` y `CMD ["pytest"]`: construir `mis-tests`, ejecutar, cambiar un `assert`, reconstruir (no reinstala pytest) y volver a ejecutar. Cualquier compañero con Docker ejecuta tus tests con los mismos dos comandos, sin tener Python ni pytest instalados.

**Extra:** añadir `precio_con_iva(precio, iva)` (`precio * (1 + iva / 100)`) y su test; añadir `colorama` a `requirements.txt` y reconstruir: ahora **sí** se repite el `RUN pip install` porque cambió `requirements.txt`.

## 3. Bind mounts

**Problema:** `COPY . .` mete en la imagen una *copia* del código. Si lo editas, el contenedor sigue ejecutando la versión antigua hasta que hagas `docker build` otra vez.

**Bind mount:** conecta una carpeta de tu ordenador con una carpeta del contenedor. No se copia nada: es la misma carpeta vista desde dos sitios.

```bash
docker run -v .:/app mi-app
```

`-v tu_carpeta:carpeta_del_contenedor` (el punto es la carpeta actual). Cambias `main.py`, guardas, relanzas el mismo comando y ves el resultado nuevo **sin `docker build`**.

| Arrancas con… | Tu carpeta | Para qué sirve |
|---|---|---|
| `-v .:/app` | La actual | Editar y ejecutar sin reconstruir |
| `-v ./tests:/app/tests` | `tests/` | Editar un test y relanzarlo al momento |
| `-v ./datos:/app/datos` | `datos/` | Lo que guarda el programa aparece en tu ordenador |

**Práctica 2:** construir `mi-app`, cambiar el print y ejecutar sin reconstruir (no cambia); ejecutar con `-v .:/app` (sí cambia). Con `mis-tests`: `docker run --rm -v .:/app mis-tests`, añadir un test (p. ej. descuento del 100 % → 0) y se ejecuta sin reconstruir; sin bind mount, la imagen conserva los archivos de cuando se construyó.

## 4. ENTRYPOINT y CMD

| | CMD | ENTRYPOINT |
|---|---|---|
| Qué es | Comando por defecto | Ejecutable fijo del contenedor |
| Si escribes algo tras la imagen en `docker run` | Lo **sustituye por completo** | Se **añade como argumentos** |
| Juntos | Argumentos por defecto | Programa que siempre se ejecuta |

```python
# main.py
import sys
print(f"Hola {sys.argv[1]}")
```

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY main.py .
ENTRYPOINT ["python", "main.py"]
CMD ["Mundo"]
```

```bash
docker build -t saludo .
docker run saludo          # Hola Mundo
docker run saludo Sofia    # Hola Sofia
```

Con solo `CMD ["python", "main.py", "mundo"]`, `docker run saludo Sofia` sustituye todo el CMD e intenta ejecutar `Sofia` como programa y falla; habría que escribir `docker run saludo python main.py Sofia`.

Ejemplo del test: con `ENTRYPOINT ["echo", "Hola"]` y `CMD ["mundo"]`, `docker run saludo clase` imprime **`Hola clase`**.

**Extra (`doble.py`):** con `ENTRYPOINT ["python", "doble.py"]` y `CMD ["5"]`: `docker run doble` → 10; `docker run doble 8` → 16; `docker run doble 20` → 40.

## 5. Un entorno Linux en un contenedor

**Un contenedor vive mientras vive su proceso principal.** Un script termina y el contenedor queda *Exited*; una terminal (`bash`) espera comandos y el contenedor sigue *Up*.

```bash
docker run -it --name mi-linux ubuntu
# root@3f2a1b9c7d10:/#   → estás dentro, como root
```

- `-it`: interactivo con terminal. `--name`: nombre. `ubuntu`: imagen oficial.
- Dentro hay un Linux real, casi vacío: instalas con apt.

```bash
cat /etc/os-release
apt update
apt install -y git
git --version
```

### Ciclo de vida

`imagen --run--> en ejecución --stop--> detenido --rm--> eliminado`

| Quiero… | Comando |
|---|---|
| Salir (detiene el contenedor) | `exit` |
| Ver todos, también detenidos | `docker ps -a` |
| Volver a entrar al mismo contenedor | `docker start -ai mi-linux` (`-a` attach, `-i` interactivo) |
| Arrancarlo en segundo plano | `docker start mi-linux` |
| Abrir otra terminal en uno en marcha | `docker exec -it mi-linux bash` (al salir no se detiene) |
| Detener | `docker stop mi-linux` |
| Eliminar (la imagen permanece) | `docker rm mi-linux` |
| Detener y eliminar de una vez | `docker rm -f mi-linux` |

`start` reutiliza el contenedor existente (git sigue instalado); `run` crearía uno nuevo y vacío. Si eliminas el contenedor, **lo instalado a mano se pierde**.

### Conservar el entorno: instalarlo en el Dockerfile

```dockerfile
FROM ubuntu
RUN apt update && apt install -y git
CMD ["bash"]
```

`&&` encadena comandos; `-y` responde «sí» porque durante el build nadie puede contestar. Cada contenedor de `mi-linux-git` tendrá git desde el principio.

Orden de comandos del ejercicio: `docker run -it --name mi-linux ubuntu` → `exit` → `docker ps -a` → `docker start mi-linux` → `docker exec -it mi-linux bash`.

**Práctica 4 (extra):** el archivo `/root/nota.txt` sobrevive a `exit` + `docker start -ai` (mismo contenedor), pero no existe en un contenedor nuevo tras `docker rm`: nunca se añadió a la imagen.

## 6. Servidores web y puertos

- **Cliente** (navegador) pide; **servidor** responde. Un **servidor web** es un programa que no termina: espera peticiones y envía la página.
- **Nginx** es un servidor web ya hecho: le das una carpeta con HTML y la sirve. Imagen oficial `nginx`.
- Un **puerto** es el número que dice a qué programa va cada petición; un puerto solo lo usa un programa a la vez.

| Puerto | Quién escucha |
|---|---|
| 80 | Páginas web (HTTP; el navegador lo usa por defecto) |
| 443 | Páginas web seguras (HTTPS) |
| 5432 | PostgreSQL |
| 3000, 8000, 8080 | Aplicaciones en desarrollo |

`localhost` es tu propio ordenador: `localhost:8080` = «en mi ordenador, el programa del puerto 8080».

### Primera web con Nginx

```html
<!-- index.html -->
<h1>Mi primer servidor con Docker</h1>
```

```dockerfile
FROM nginx:alpine
WORKDIR /usr/share/nginx/html/
COPY . .
EXPOSE 80
```

`EXPOSE 80` solo informa del puerto; publicarlo se hace al arrancar. No hace falta `CMD`: la imagen de Nginx ya trae el suyo.

```bash
docker build -t mi-web .
docker run -d -p 8080:80 --name web-docker mi-web
docker ps       # PORTS: 0.0.0.0:8080->80/tcp
```

- `-d`: segundo plano (un servidor no termina; si no, te quedas sin terminal).
- `-p 8080:80`: **tu ordenador : contenedor**. 8080 es lo que escribes en el navegador (`http://localhost:8080`); 80 es donde escucha Nginx. Mismo orden que `-v`.

| Arrancas con… | Abres | Llega al contenedor por |
|---|---|---|
| `-p 8080:80` | `localhost:8080` | 80 |
| `-p 3000:80` | `localhost:3000` | 80 |
| `-p 80:80` | `localhost` | 80 |
| `-p 8080:8000` | `localhost:8080` | 8000 (app Python) |
| (sin `-p`) | No se puede abrir | El servidor funciona, pero nadie llega a él |

**Extra:** con bind mount, `docker run -d -p 8080:80 --name web-docker -v ./index.html:/usr/share/nginx/html/index.html:ro mi-web` (`:ro` = solo lectura) y los cambios al HTML se ven al recargar.

**Reto:** `web1` (`-p 8081:80`) y `web2` (`-p 8082:80`) desde la misma imagen = 1 imagen y 2 contenedores independientes. `web3` con `-p 8081:80` falla porque el puerto 8081 ya lo usa `web1`.

## 7. Inspección de errores

`crash.py` falla a propósito:

```python
print("Arrancando…")
numeros = [1, 2, 3]
print(numeros[5])
```

Lanzado con `-d` no se ve nada y `docker ps` sale vacío: el contenedor terminó con error.

| Comando | Qué te dice |
|---|---|
| `docker ps -a` | Estado del contenedor (`Exited (1)` = terminó con error) |
| `docker logs mi-crash` | Todo lo que escribió, incluido el error de Python |
| `docker rm -f mi-crash` | Lo elimina para poder repetir el nombre |

**Código de salida:** `Exited (0)` = terminó bien; `Exited (1)` = terminó con error → mirar `docker logs`.

**Práctica 6:** construir `crash`, `docker run -d --name mi-crash crash`, `docker ps -a`, `docker logs mi-crash`, `docker rm`, corregir y comprobar `Exited (0)`. **Extra:** `division.py` con `print(10 / 0)` produce `ZeroDivisionError` (código 1); con `10 / 2` imprime `5.0` y termina con `Exited (0)`.

## 8. Chuleta y errores frecuentes

| Comando | Para qué sirve |
|---|---|
| `docker run -it --name mi-linux ubuntu` | Crear un contenedor y entrar en su terminal |
| `docker start -ai mi-linux` | Volver a entrar en uno detenido |
| `docker exec -it mi-linux bash` | Abrir terminal en uno en marcha |
| `docker run -d -p 8080:80 mi-web` | Segundo plano publicando un puerto |
| `docker rm -f web-docker` | Eliminar aunque esté en marcha |
| `docker logs mi-crash` | Ver lo que ha escrito un contenedor |

| Lo que ves | Causa | Solución |
|---|---|---|
| `…port is already allocated` | Puerto del ordenador ocupado | Usar otro (`-p 8081:80`) o eliminar el contenedor que lo usa |
| `…name … is already in use` | Ya hay un contenedor con ese nombre | `docker rm nombre` o usar otro nombre |
| La página no carga | Falta `-p`, puerto equivocado o contenedor detenido | Mirar `docker ps`: estado y columna PORTS |
| `"pytest": executable file not found` | `pytest` no está en `requirements.txt` o no reconstruiste | Añadirlo y `docker build` |

**Preguntas de autoevaluación:** diferencia entre RUN y CMD y entre CMD y ENTRYPOINT; por qué se copia `requirements.txt` antes; para qué sirve un bind mount mientras programas; qué pasa con lo instalado dentro de un contenedor al eliminarlo; qué es un servidor web y qué significa cada número en `-p 8080:80`; qué dos comandos (`docker ps -a` y `docker logs`) usar cuando un contenedor se para solo.
