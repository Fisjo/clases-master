# Clase Docker 1 · Fundamentos

Explicación organizada de la presentación **Docker 1** (Máster en Desarrollo Web, IA aplicada y DevOps · EDEM, Sofía Pinilla). Esta clase es puramente conceptual y de primeros comandos: no hay código en la carpeta, solo esta guía.

## Objetivos

1. Entender qué es el **kernel** y por qué es la pieza clave.
2. Entender qué es una **máquina virtual**, cómo funciona un hipervisor y cuándo usarla.
3. Entender qué es **Docker**, en qué se diferencia de una VM y qué ventajas tiene.
4. **Dockerizar un script de Python**.

## Índice

1. [El problema de partida](#1-el-problema-de-partida)
2. [Hardware, kernel y sistema operativo](#2-hardware-kernel-y-sistema-operativo)
3. [Máquinas virtuales](#3-máquinas-virtuales)
4. [¿Qué es un entorno?](#4-qué-es-un-entorno)
5. [¿Qué es Docker?](#5-qué-es-docker)
6. [Dockerfile → imagen → contenedor](#6-dockerfile--imagen--contenedor)
7. [Docker Hub](#7-docker-hub)
8. [Nuestro primer Dockerfile](#8-nuestro-primer-dockerfile)
9. [Chuleta de comandos y errores frecuentes](#9-chuleta-de-comandos-y-errores-frecuentes)
10. [Ejercicios de la clase](#10-ejercicios-de-la-clase)

---

## 1. El problema de partida

> «Pues en mi ordenador funciona…»

Un programa que funciona en una máquina y falla en la de un compañero. La causa casi siempre es que **el entorno es distinto** (versión de Python, librerías, sistema operativo…). Docker nace para llevar *el mismo entorno a todas partes*.

## 2. Hardware, kernel y sistema operativo

Un ordenador funciona **por capas**, y cada capa usa los servicios de la de abajo:

| Capa | Contenido |
|---|---|
| Aplicaciones | Navegador, VS Code, tu script de Python |
| Espacio de usuario | Librerías, terminal (bash), utilidades, configuración |
| **Kernel** | Gestiona procesos, memoria, disco y red |
| Hardware | CPU, RAM, disco, tarjeta de red |

- **Sistema operativo = kernel + espacio de usuario.**
- Las aplicaciones **nunca tocan el hardware directamente**: se lo piden al kernel. El kernel es el único programa con acceso directo al hardware.

**Analogía del restaurante:** clientes = aplicaciones (piden cosas), camarero = kernel (recoge pedidos, decide el orden, reparte recursos; nadie más entra en la cocina), cocina = hardware (hace el trabajo real).

### Los cuatro trabajos del kernel

| Trabajo | Qué hace |
|---|---|
| Procesos | Arranca y detiene programas y reparte el tiempo de CPU |
| Memoria | Asigna RAM a cada proceso e impide que uno lea la de otro |
| Archivos | Lee y escribe en disco y controla permisos |
| Dispositivos y red | Habla con teclado, pantalla, USB y red mediante *drivers* |

### Llamadas al sistema (syscalls)

Una *syscall* es la forma en que un programa le pide algo al kernel (abrir un archivo, reservar memoria, escribir en pantalla). Al ejecutar `print("Hola")`:

`tu código → intérprete Python → syscall write() → el kernel lo atiende → terminal`

**Clave para Docker:** un programa dentro de un contenedor hace sus syscalls **al kernel del host**. No hay otro kernel.

## 3. Máquinas virtuales

Una **máquina virtual (VM)** usa los recursos de un ordenador físico para simular otro ordenador completo, **con su propio kernel**.

### Para qué se usa

| Uso | Ejemplo |
|---|---|
| Software antiguo | Una app que solo funciona en Windows XP |
| Probar otro sistema | Aprender Linux desde Windows sin tocar el sistema principal |
| Seguridad | Abrir un archivo sospechoso en una VM aislada |
| La nube | Un servidor físico dividido en muchas VMs alquiladas |

### Las tres piezas

| Papel | Nombre | Qué es |
|---|---|---|
| El anfitrión | **Host** | El ordenador físico real (pone CPU, RAM, disco) |
| El repartidor | **Hipervisor** | Software que crea las VMs y les reparte CPU, memoria y disco virtuales (VirtualBox, VMware, Hyper-V…) |
| El invitado | **Guest** | La VM: arranca su propio SO con su propio kernel |

Tres VMs en un portátil = **cuatro kernels** funcionando (el del host + uno por VM). Se pueden mezclar sistemas (Windows dentro de Mac, Linux dentro de Windows…).

### Pros y contras

| Ventajas | Inconvenientes |
|---|---|
| Aislamiento muy fuerte (cada VM tiene su kernel) | Pesada: varios GB |
| Cualquier sistema operativo en el mismo host | Lenta al arrancar (arranca un SO completo) |
| Instantáneas (*snapshots*) para volver atrás | Reserva recursos aunque no los use |

## 4. ¿Qué es un entorno?

> La misma receta (tu código) en otra cocina (el entorno) puede salir distinta.

El **entorno** es todo lo que rodea a tu código y que necesita para funcionar:

| Pieza | Ejemplo |
|---|---|
| Sistema operativo | Debian, Windows 11, macOS |
| Lenguaje y versión | Python 3.11 (no 3.7 ni 3.12) |
| Librerías y versiones | pandas, requests, flask… en versión concreta |
| Variables de entorno | `DB_PASSWORD`, `API_KEY` |
| Configuración y archivos | `config.yaml`, carpeta de datos, zona horaria |

Entornos habituales: **desarrollo** (tu portátil), **pruebas** (servidor previo a publicar) y **producción** (el que usan los clientes). El monitor conectado, por ejemplo, *no* forma parte del entorno de ejecución.

## 5. ¿Qué es Docker?

Docker **empaqueta una aplicación con todo lo que necesita** y la ejecuta en un **contenedor aislado que comparte el kernel** del sistema anfitrión.

**Caso Andrea y Pablo.** Andrea desarrolla con Python 3.7.5; Pablo tiene 3.11 y la librería es incompatible → error y el clásico «en mi ordenador funciona». Con Docker, Andrea sube un Dockerfile al repositorio junto al código, Pablo construye la imagen y ejecuta un contenedor; Python 3.7.5 va *dentro de la imagen*, así que Pablo no lo instala y sus proyectos con 3.11 siguen intactos. (Reduce mucho las diferencias, aunque la arquitectura del procesador y la configuración externa también cuentan.)

Dentro del paquete va: tu código, el lenguaje y las dependencias. **El kernel NO va dentro.**

### VM vs contenedor

| Aspecto | Máquina virtual | Contenedor |
|---|---|---|
| Qué virtualiza | El hardware completo | El entorno de la aplicación |
| Kernel | Propio, uno por VM | Compartido con el host |
| Tamaño típico | Gigabytes | Megabytes |
| Arranque | Un SO entero | Un proceso: casi inmediato |
| Aislamiento | Muy fuerte | Fuerte, pero comparte kernel |
| Sistemas posibles | Cualquiera | Los compatibles con el kernel del host |

Con VMs hay 4 kernels; con contenedores, **1 kernel** y cada contenedor es solo un proceso aislado.

### Docker Desktop en Windows/Mac

Docker Desktop **crea una pequeña VM Linux** (WSL 2 en Windows) y ejecuta ahí los contenedores. Por eso hay que **abrir Docker Desktop antes de usar Docker**: sin esa VM no hay kernel Linux.

### Lo que Docker no resuelve

| Límite | Significado |
|---|---|
| No cambia el kernel | Un contenedor Linux no ejecuta una app de Windows (para eso, una VM) |
| Aislamiento menor que una VM | Un fallo grave del kernel afecta a todos los contenedores |
| Los datos no se guardan solos | Si borras un contenedor, se pierde lo que escribió (se resuelve con volúmenes) |
| No arregla código roto | Si falla, falla también en el contenedor |

## 6. Dockerfile → imagen → contenedor

| Docker | Qué es | Cocina |
|---|---|---|
| **Dockerfile** | Archivo de texto con instrucciones para construir una imagen (`docker build`) | La receta |
| **Imagen** | Plantilla de solo lectura con código, dependencias y configuración (`docker run` la pone en marcha) | El plato preparado y congelado |
| **Contenedor** | Instancia en marcha de la imagen, con su propio estado (en ejecución o detenido) | El plato descongelado y servido |

De una imagen se pueden crear muchos contenedores, como de un molde salen muchas piezas.

## 7. Docker Hub

Docker Hub es a las imágenes lo que GitHub es al código. Si una imagen no está en tu ordenador, `docker run` o `docker build` la descargan solos.

- Imagen oficial: `python:3.11-slim` → `nombre:etiqueta` (versión y variante).
- Imagen de usuario: `sofia/mi-app:1.0` → `usuario/nombre:etiqueta`.
- Sin etiqueta se usa `latest`.

```bash
docker pull python:3.11-slim    # descargar sin ejecutar
```

### Variantes de la imagen de Python

| Variante | Cuándo |
|---|---|
| Estándar | Quiero que funcione fácil y tener herramientas disponibles |
| `slim` | Una app más ligera sin perder compatibilidad habitual de Debian |
| `alpine` | Minimizar tamaño, sabiendo que mis dependencias son compatibles |

Menos tamaño = descargas más rápidas y menos que mantener. (Ejercicio 2: descargar las tres, `docker images python` y comparar la columna SIZE.)

## 8. Nuestro primer Dockerfile

Antes de empezar: Docker Desktop abierto, carpeta `mi-primer-docker` abierta en VS Code, terminal en ella y comprobar con:

```bash
docker --version
docker run hello-world     # descarga y ejecuta una prueba completa
```

**Paso 1 · `main.py`**

```python
print("Soy un crack en Docker")
```

**Paso 2 · `Dockerfile`** (sin extensión)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
CMD ["python", "main.py"]
```

| Instrucción | Función |
|---|---|
| `FROM` | Imagen base oficial que ya trae Python 3.11 |
| `WORKDIR` | Directorio de trabajo dentro de la imagen (se crea si no existe) |
| `COPY . .` | Copia tu carpeta (primer punto) a `/app` dentro de la imagen (segundo punto) |
| `CMD` | Comando de arranque del contenedor |

Orden correcto: base primero, luego dónde trabajar, después qué copiar y al final cómo arrancar.

**Paso 3 · Construir la imagen**

```bash
docker build -t mi-app .
docker images
```

`-t mi-app` da nombre a la imagen y `.` es el contexto (esta carpeta).

**Paso 4 · Ejecutar el contenedor**

```bash
docker run --name mi-contenedor mi-app:latest
# Soy un crack en Docker
```

La imagen se llama `mi-app`; el contenedor, `mi-contenedor`: son cosas distintas. El contenedor se detiene porque su proceso principal (el script) termina.

**Variante con dependencias** (Dockerfile de Andrea): `RUN` va después de `COPY` porque necesita que `requirements.txt` ya esté dentro, y `CMD` siempre al final.

```dockerfile
FROM python:3.7.5-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## 9. Chuleta de comandos y errores frecuentes

| Comando | Para qué sirve |
|---|---|
| `docker pull python:3.11-slim` | Descargar una imagen de Docker Hub |
| `docker build -t mi-app:1.0 .` | Construir una imagen desde el Dockerfile |
| `docker images` | Ver imágenes |
| `docker run --name mi-contenedor mi-app:1.0` | Crear y arrancar un contenedor |
| `docker ps` | Ver contenedores en ejecución |
| `docker ps -a` | Ver todos los contenedores |

| El mensaje dice… | Causa | Solución |
|---|---|---|
| `Cannot connect to the Docker daemon…` | Docker Desktop cerrado | Abrirlo y esperar |
| `"docker build" requires exactly 1 argument` | Falta el punto final | `docker build -t mi-app .` |
| `…open Dockerfile: no such file…` | Carpeta equivocada o `Dockerfile.txt` | Ir a la carpeta / renombrar |
| `can't open file '/app/main.py'` | `main.py` no se copió a la imagen | Revisar nombre, carpeta y `COPY`; reconstruir |

## 10. Ejercicios de la clase

**Ejercicio 1 · ¿VM o contenedor?**

| Caso | Mejor con… |
|---|---|
| Ejecutar la API del equipo igual en todos los portátiles | Contenedor |
| Probar Windows 11 desde tu Mac | Máquina virtual |
| Lanzar 20 copias de un servidor web | Contenedor |
| Abrir un archivo sospechoso con máximo aislamiento | Máquina virtual |
| Probar un script con Python 3.8 y 3.12 sin instalar nada | Contenedor |
| Programa antiguo solo para Windows XP | Máquina virtual |

**Práctica 1 · «Soy un crack en Docker»:** crear `main.py` y `Dockerfile`, construir `mi-app:latest`, comprobarla en `docker images`, ejecutar `mi-contenedor` en primer plano y explicar por qué el contenedor se detiene (el proceso principal termina).

**Preguntas de repaso (respuestas):** la finalidad de un contenedor es ejecutar una aplicación en un entorno aislado basado en una imagen; es más ligero que una VM porque comparte el kernel del host; el flujo es Dockerfile → imagen → contenedor; lo que ayuda con «en mi ordenador funciona» es usar una imagen con la app y sus dependencias.
