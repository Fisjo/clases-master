"""
Clase 3 de Python: inputs, casting, round, break/continue, errores y módulos.

Contenido:
    1. Inputs
    2. Casting
    3. Round
    4. Break y continue
        4.1 continue
        4.2 break
        4.3 Ejercicios
    5. Try y except
        5.1 Captura básica
        5.2 Varios errores y finally
        5.3 Reintentar con un bucle
    6. Módulos
    7. Tests
"""

# =============================================================================
# 1. INPUTS
# =============================================================================

# Un input es una función que permite al usuario ingresar datos desde la
# consola. En Python se utiliza `input()`: muestra un mensaje, espera a que el
# usuario escriba y devuelve lo escrito SIEMPRE como string (`str`).
nombre = input("Por favor, ingresa tu nombre: ")
print(f"Hola, {nombre}! Bienvenido/a a la clase de Python.")

# Para trabajar con números hay que convertir el texto (ver sección 2).
edad = int(input("Por favor, ingresa tu edad: "))
print(f"Tienes {edad} años.")

numero1 = float(input("Ingresa un número decimal: "))
numero2 = float(input("Ingresa otro número decimal: "))
suma = numero1 + numero2
print(f"La suma de {numero1} y {numero2} es: {suma}")


# =============================================================================
# 2. CASTING
# =============================================================================

# El casting es el proceso de convertir un tipo de dato a otro. Se realiza con
# funciones como `int()`, `float()` y `str()`.
print(int("123"))        # 123     -> convierte el string "123" a entero
print(float("123.45"))   # 123.45  -> convierte el string "123.45" a decimal
print(str(123))          # 123     -> convierte el entero 123 a string

# Si el valor no se puede convertir (por ejemplo int("hola")), Python lanza un
# `ValueError`. Se gestiona con try/except (ver sección 5).


# =============================================================================
# 3. ROUND
# =============================================================================

# `round(numero, decimales)` redondea un número decimal. Si no se indican los
# decimales, devuelve un entero.
# Con el .5 exacto, Python redondea al número PAR más cercano (redondeo
# bancario), no siempre hacia arriba.
print(round(3.14159, 2))  # 3.14 -> redondea a 2 decimales
print(round(2.71828))     # 3    -> redondea al entero más cercano
print(round(2.5))         # 2    -> redondeo bancario (par más cercano)
print(round(3.5))         # 4    -> redondeo bancario (par más cercano)


# =============================================================================
# 4. BREAK Y CONTINUE
# =============================================================================

# `break` sale del bucle antes de que termine su ejecución normal.
# `continue` salta a la siguiente iteración, omitiendo el resto del código de
# la iteración actual.

# --- 4.1 continue ---

# Salta los pares e imprime el cuadrado de los impares.
for numero in range(1, 100):  # números del 1 al 99
    if numero % 2 == 0:
        print(f"{numero} es un número par, se saltará esta iteración.")
        continue
    print(f"{numero} es un número impar, su cuadrado es {numero ** 2}.")
print("Fin del bucle.")

# --- 4.2 break ---

# Recorre la lista y se detiene al encontrar una edad de 65 o más.
lista_edades = [15, 22, 17, 30, 65, 45, 70, 19]

for edad in lista_edades:
    if edad < 18:
        continue  # salta las edades menores de 18
    if edad >= 65:
        print(f"{edad} es mayor de 65, se detendrá el bucle.")
        break  # sale del bucle
    print(f"{edad} es una edad válida para el bucle.")

# --- 4.3 Ejercicios ---

# Encontrar el último número primo menor que 100.
# Un número es primo si no tiene divisores entre 2 y su raíz cuadrada.
print("Objetivo: encontrar el último número primo menor a 100")
for numero in range(1, 100):
    if numero < 2:
        continue  # los números menores que 2 no son primos
    es_primo = True
    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            es_primo = False
            break  # sale del bucle interno en cuanto encuentra un divisor
    if es_primo:
        ultimo_primo = numero
print(f"El último número primo menor a 100 es: {ultimo_primo}")  # 97

# Imprimir los múltiplos de 5 y parar cuando un número supere 150.
numeros = [12, 15, 32, 42, 55, 75, 122, 132, 150, 180, 200]

for numero in numeros:
    if numero > 150:
        break
    if numero % 5 == 0:
        print(numero)  # Salida: 15, 55, 75, 150


# =============================================================================
# 5. TRY Y EXCEPT
# =============================================================================

# La estructura `try` / `except` permite manejar excepciones: se ejecuta un
# bloque de código y, si ocurre un error, se captura para que el programa no se
# detenga de golpe.

# --- 5.1 Captura básica ---
try:
    resultado = 10 / 0  # genera un error de división por cero
except ZeroDivisionError:
    print("Error: No se puede dividir por cero.")

# --- 5.2 Varios errores y finally ---
# Se pueden encadenar varios `except`, uno por cada tipo de error.
# El bloque `finally` se ejecuta SIEMPRE, haya error o no.
try:
    numero1 = int(input("Ingresa un número entero: "))
    numero2 = int(input("Ingresa otro número entero: "))
    resultado = numero1 / numero2
    print(f"El resultado de {numero1} dividido por {numero2} es: {resultado}")
except ValueError:
    print("Error: Debes ingresar un número entero válido.")
except ZeroDivisionError:
    print("Error: No se puede dividir por cero.")
finally:
    print("Gracias por usar el programa de división.")

# --- 5.3 Reintentar con un bucle ---
# Pide un entero hasta 5 veces: cada fallo suma un intento y, si la entrada es
# válida, `break` sale del bucle.
contador = 0
while contador < 5:
    try:
        numero = int(input("Ingresa un número entero: "))
        print(f"Has ingresado el número: {numero}")
        break  # sale del bucle si la entrada es válida
    except ValueError:
        contador += 1
        print(f"Error: Debes ingresar un número entero válido. Intentos restantes: {5 - contador}")


# =============================================================================
# 6. MÓDULOS
# =============================================================================

# Un módulo es un archivo `.py` que contiene definiciones y declaraciones de
# Python. Los módulos permiten organizar el código en partes reutilizables y
# mantenerlo limpio. Se importan con la palabra clave `import`.
#
# Los módulos de esta clase están en la carpeta `modules/`:
#   - mates.py:   sumar, restar, multiplicar y dividir
#   - saludos.py: saludo y despedir
import modules.mates
import modules.saludos

print(modules.mates.sumar(5, 3))        # 8
print(modules.mates.restar(10, 4))      # 6
print(modules.mates.multiplicar(6, 7))  # 42
print(modules.mates.dividir(8, 2))      # 4.0
print(modules.mates.dividir(8, 0))      # muestra el error y luego None

# `saludo` y `despedir` imprimen el mensaje y no devuelven nada, por eso al
# envolverlas en `print()` aparece además `None`.
print(modules.saludos.despedir("Nacho"))  # Adios Nacho / None
print(modules.saludos.saludo("Nacho"))    # Hola Nacho! / None


# =============================================================================
# 7. TESTS
# =============================================================================

# Un test es una función que comprueba con `assert` que otra función devuelve
# lo esperado. Si el `assert` falla, el test falla.
#
# En `modules/precios.py` está la función `precio_descuento(precio, descuento)`
# y en `modules/test_precios.py` sus tests. Los floats no se comparan con `==`
# (100 * (1 - 0.3) puede dar 70.00000000000001), se usa `math.isclose`.
#
# Para ejecutarlos (requiere `pip install pytest`):
#     cd clase-python3/modules
#     pytest

alumnos = [
    {"nombre": "Ana", "nota": 8.5},
    {"nombre": "Luis", "nota": 4.0},
    {"nombre": "Marta", "nota": 7.0},
    {"nombre": "Pablo", "nota": 3.5},
    {"nombre": "Sara", "nota": 9.0},
]

def calcular_media(alumnos:list)->float:
    """Calcula la media de una lista de alumnos
    Args:
        alumnos (list): Lista de objetos de estudiantes
    Returns:
        float: Media de las notas de los estudiantes
    """
    media = 0

    sumaNotas = 0
    for alumno in alumnos:
        nota = alumno["nota"]
        sumaNotas += float(nota)

    media = round(sumaNotas/len(alumnos), 2)
    return media

contAprob = 0
for alumno in alumnos:
    nota = alumno["nota"]

    if nota >= 5:
        estado = "Aprobad@"
        contAprob += 1
    else: 
        estado = "Suspens@"
    
    print(f"{alumno["nombre"].upper()}: {nota} -> {estado} ")

    

print(f"\nTotal estudiantes: {len(alumnos)}")
print(f"Estudiantes aprobadxs: {contAprob}")
print(f"Estudiantes suspensxs: {len(alumnos) - contAprob}")
print(f"Media de la clase: {calcular_media(alumnos)}")