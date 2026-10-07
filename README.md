# Repositorio de clases de Máster de IA, Data & Cloud @ EDEM Escuela de Empresarios

Este repositorio es un conjunto de ejercicios prácticos para aprender Python y, además, una pequeña práctica de trabajo con Git. No se trata de un proyecto de producción, sino de un espacio para probar conceptos básicos de programación, manipular variables, escribir funciones y familiarizarse con el flujo de trabajo de control de versiones.

## Estructura del repositorio

- `clase-python1/holamundo.py`: archivo principal de práctica de Python. Aquí se trabajan conceptos básicos como:
  - variables
  - cadenas de texto
  - listas y diccionarios
  - tuplas
  - operadores
  - condicionales
  - comparaciones y asignaciones

- `clase-python2/class.py`: segunda clase de Python. Se trabajan:
  - sets
  - repaso de diccionarios y condicionales
  - bucles (`for` y `while`)
  - funciones (básicas, docstrings, parámetros por defecto)
  - funciones lambda

- `clase-python3/clase3.py`: tercera clase de Python. Se trabajan:
  - entrada de datos con `input()`
  - casting (conversión de tipos)
  - redondeo con `round()`
  - control de bucles con `break` y `continue`
  - manejo de errores con `try`, `except` y `finally`
  - módulos propios (`clase-python3/modules/`)

- `clase-git/`: carpeta creada principalmente como ejercicio de Git. En ella hay varios archivos y scripts sencillos, pero su objetivo real era practicar:
  - ramas
  - commits
  - merges
  - pull requests
  - resolución de conflictos
  - flujo de trabajo colaborativo

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
- escritura de funciones simples
- entrada y salida por consola
- lógica de programación básica
- trabajo con Git y GitHub en equipo

## Requisitos

Necesitas tener instalado:

- Python 3
- Git

## Cómo ejecutarlo

Para ejecutar los scripts de la carpeta de Git:

```bash
cd clase-git
python3 app.py
python3 interes-compuesto.py
python3 numeros-aleatorios.py
```

Para ejecutar el ejemplo introductorio de Python:

```bash
cd clase-python1
python3 holamundo.py
```

Para ejecutar la segunda clase de Python:

```bash
cd clase-python2
python3 class.py
```

Para ejecutar la tercera clase de Python (pide datos por consola mediante `input()`):

```bash
cd clase-python3
python3 clase3.py
```

## Detalle de la clase 3 (`clase-python3`)

El archivo `clase3.py` está dividido en secciones, cada una con su cabecera `## TEMA ##`.

### 1. Inputs

`input()` pausa el programa, muestra un mensaje y devuelve lo que escribe el usuario **siempre como texto (`str`)**. Por eso, para operar con números hay que convertirlo:

```python
nombre = input("Por favor, ingresa tu nombre: ")
edad = int(input("Por favor, ingresa tu edad: "))        # entero
numero1 = float(input("Ingresa un número decimal: "))    # decimal
print(f"La suma es: {numero1 + numero2}")
```

También se usan las *f-strings* (`f"Hola, {nombre}!"`) para insertar variables dentro de un texto.

### 2. Casting

Convertir un valor de un tipo a otro con `int()`, `float()` y `str()`:

```python
print(int("123"))       # 123      (str -> int)
print(float("123.45"))  # 123.45   (str -> float)
print(str(123))         # "123"    (int -> str)
```

Si el valor no se puede convertir (por ejemplo `int("hola")`) Python lanza un `ValueError`, que se gestiona más adelante con `try`/`except`.

### 3. Round

`round(numero, decimales)` redondea un número. Sin el segundo argumento devuelve un entero.

```python
round(3.14159, 2)  # 3.14
round(2.71828)     # 3
round(2.5)         # 2  (redondeo bancario: al par más cercano)
round(3.5)         # 4
```

Cuando el decimal es exactamente `.5`, Python redondea al **número par más cercano** (*redondeo bancario*), no siempre hacia arriba. Por eso `2.5` da `2` y `3.5` da `4`.

### 4. Break y Continue

- `break`: sale del bucle por completo.
- `continue`: salta a la siguiente iteración, ignorando el resto del código del ciclo actual.

Ejemplos de la clase:

- **Pares e impares**: recorre `range(1, 100)`; con `continue` salta los pares e imprime el cuadrado de los impares.
- **Último primo menor a 100**: para cada número comprueba si tiene divisores entre `2` y su raíz cuadrada (`int(numero ** 0.5) + 1`). Si encuentra uno, marca `es_primo = False` y hace `break` del bucle interno. Se descartan con `continue` los números menores que 2 y se guarda el último primo encontrado.
- **Lista de edades**: ignora (`continue`) las menores de 18 y detiene el bucle (`break`) al encontrar una edad de 65 o más.
- **Múltiplos de 5**: recorre una lista, para (`break`) cuando un número supera 150 e imprime los que son múltiplos de 5.

### 5. Try y Except

Permite capturar errores en tiempo de ejecución para que el programa no se detenga de golpe.

```python
try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Error: No se puede dividir por cero.")
```

Estructura completa:

- `try`: código que puede fallar.
- `except TipoDeError`: qué hacer si ocurre ese error concreto (se pueden encadenar varios, p. ej. `ValueError` y `ZeroDivisionError`).
- `finally`: se ejecuta **siempre**, haya error o no.

La clase incluye una calculadora de división que pide dos enteros y controla los dos errores posibles, y un bucle `while` que reintenta hasta 5 veces pedir un entero válido: si hay `ValueError` suma uno al contador, y si la entrada es correcta sale con `break`.

### 6. Modules

Un módulo es un archivo `.py` con funciones reutilizables. Permite dividir el código en partes y mantenerlo ordenado. Se carga con `import`.

La carpeta `clase-python3/modules/` contiene:

- `mates.py`: `sumar`, `restar`, `multiplicar` y `dividir` (esta última controla la división por cero con `try`/`except`).
- `saludos.py`: `saludo(nombre)` y `despedir(nombre)`.

Uso desde `clase3.py`:

```python
import modules.mates
import modules.saludos

print(modules.mates.sumar(5, 3))      # 8
print(modules.mates.dividir(8, 0))    # muestra el error y luego None
print(modules.saludos.saludo("Nacho"))
```

Detalle a tener en cuenta: `saludo`, `despedir` y `dividir` (en el caso de división por cero) no devuelven un valor, solo imprimen. Por eso, al envolver la llamada en otro `print(...)`, además del mensaje aparece `None`. Python crea la carpeta `__pycache__` automáticamente al importar módulos; no hace falta tocarla.

## Nota importante

La carpeta `clase-git` no es un proyecto funcional complejo ni un producto final. Fue principalmente una práctica para aprender a trabajar con Git, ramas, merges y pull requests. La parte más importante de ese ejercicio era el proceso de colaboración y manejo del repositorio, no la lógica del programa en sí.

## Estado del proyecto

Proyecto de aprendizaje básico, orientado a practicar programación con Python y familiarizarse con Git y GitHub en un entorno sencillo.
