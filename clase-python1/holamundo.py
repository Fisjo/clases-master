"""
Clase 1 de Python: fundamentos del lenguaje.

Contenido:
    1. Hola mundo y comentarios
    2. Variables y f-strings
    3. Tipos de datos básicos
    4. Strings: indexado y métodos
    5. Diccionarios
    6. Listas
    7. Tuplas
    8. Constantes
    9. Operadores (comparación, pertenencia y asignación)
   10. Condicionales
"""

# =============================================================================
# 1. HOLA MUNDO Y COMENTARIOS
# =============================================================================

# Esto es un comentario: Python lo ignora al ejecutar el programa.
# `print()` muestra un valor por pantalla.
print("Hola mundo")


# =============================================================================
# 2. VARIABLES Y F-STRINGS
# =============================================================================

# Una variable guarda un valor. La anotación `: str` indica el tipo esperado
# (es opcional, pero ayuda a leer y a revisar el código).
patata: str = "patata"
print(patata)

pais: str = "España"
ciudad: str = "Madrid"

# f-string: un string con prefijo `f` que permite insertar variables con {}.
print(f"Vivo en {ciudad}, {pais}")

nombre: str = "Nacho"
apellido: str = "Pinazo"
print(f"Mi nombre es {nombre} {apellido}")

# Las f-strings también sirven para construir nuevos strings.
nombre_completo: str = f"{nombre} {apellido} Orihuela"
print(f"Mi nombre completo es {nombre_completo}")


# =============================================================================
# 3. TIPOS DE DATOS BÁSICOS
# =============================================================================

# `type()` devuelve el tipo de un valor.
print(type(nombre_completo))  # <class 'str'>

n: int = 5
print(type(n))  # <class 'int'>

tengo_carnet: bool = True
print(type(tengo_carnet))  # <class 'bool'>


# =============================================================================
# 4. STRINGS: INDEXADO Y MÉTODOS
# =============================================================================

# --- Sobre "patata" ---
print(patata[1])                # a            -> índice 1 (se empieza en 0)
print(len(patata))              # 6            -> longitud del string
print(patata.upper())           # PATATA       -> a mayúsculas
print(patata.lower())           # patata       -> a minúsculas
print(patata.replace("a", "o")) # pototo       -> sustituye todas las "a" por "o"
print(patata.split("a"))        # ['p', 't', 't', ''] -> divide el string por "a"

# --- Sobre "Nacho" ---
print(nombre.upper())  # NACHO
print(len(nombre))     # 5
print(nombre[0])       # N -> primer carácter
print(apellido[-1])    # o -> índice negativo: empieza a contar desde el final


# =============================================================================
# 5. DICCIONARIOS
# =============================================================================

# Un diccionario guarda pares clave -> valor.
persona = {
    "nombre": "Nacho",
    "apellido": "Pinazo",
    "edad": 30,
    "ciudad": "Madrid",
    "soltero": True,
}

# Acceso por clave con corchetes (da error si la clave no existe).
print(persona["nombre"])   # Nacho
print(persona["edad"])     # 30
print(persona["ciudad"])   # Madrid
print(persona["soltero"])  # True

# Acceso con .get() (devuelve None si la clave no existe, sin dar error).
nombre_diccionario = persona.get("nombre")
print(nombre_diccionario)  # Nacho


# =============================================================================
# 6. LISTAS
# =============================================================================

# Una lista es una colección ordenada y modificable.
frutas = ["manzana", "pera", "plátano", "naranja"]

# --- Acceso por índice ---
print(frutas[0])  # manzana
print(frutas[1])  # pera
print(frutas[2])  # plátano
print(frutas[3])  # naranja

print(len(frutas))  # 4 -> número de elementos
print(frutas)       # ['manzana', 'pera', 'plátano', 'naranja']

# --- Slicing: lista[inicio:fin] (el fin no se incluye) ---
print(frutas[0:2])  # ['manzana', 'pera']
print(frutas[1:])   # ['pera', 'plátano', 'naranja']
print(frutas[:3])   # ['manzana', 'pera', 'plátano']
print(frutas[-1])   # naranja -> último elemento

# --- Modificar la lista ---
frutas.append("kiwi")  # añade "kiwi" al final
print(frutas)          # ['manzana', 'pera', 'plátano', 'naranja', 'kiwi']

frutas.insert(1, "sandía")  # inserta "sandía" en la posición 1
print(frutas)               # ['manzana', 'sandía', 'pera', 'plátano', 'naranja', 'kiwi']

frutas.remove("pera")  # elimina la primera aparición de "pera"
print(frutas)          # ['manzana', 'sandía', 'plátano', 'naranja', 'kiwi']

frutas.pop()   # elimina el último elemento ("kiwi")
print(frutas)  # ['manzana', 'sandía', 'plátano', 'naranja']

frutas.sort()  # ordena alfabéticamente (modifica la lista original)
print(frutas)  # ['manzana', 'naranja', 'plátano', 'sandía']

frutas.reverse()  # invierte el orden (modifica la lista original)
print(frutas)     # ['sandía', 'plátano', 'naranja', 'manzana']

# --- Ejemplo: lista de la compra ---
compras = ["leche", "huevos", "pan", "mantequilla"]
compras.append("frutas")      # añade "frutas" al final
compras.insert(2, "verduras") # añade "verduras" en la posición 2
compras.pop()                 # elimina el último elemento ("frutas")
print(compras)  # ['leche', 'huevos', 'verduras', 'pan', 'mantequilla']

# sorted() devuelve una lista nueva ordenada, sin modificar la original.
compras_ordenadas = sorted(compras)
print(compras_ordenadas)  # ['huevos', 'leche', 'mantequilla', 'pan', 'verduras']


# =============================================================================
# 7. TUPLAS
# =============================================================================

# Las tuplas son inmutables: no se pueden modificar una vez creadas.
fecha_nacimiento: tuple = ("30", "06", "1993")
print(fecha_nacimiento[0])  # 30
print(fecha_nacimiento[1])  # 06
print(fecha_nacimiento[2])  # 1993


# =============================================================================
# 8. CONSTANTES
# =============================================================================

# Las constantes son variables que no cambian a lo largo del programa.
# Python no tiene una forma de declararlas, así que por convención se escribe
# su nombre en MAYÚSCULAS para indicar que no deben modificarse.
PI: float = 3.14159
IVA: float = 0.21


# =============================================================================
# 9. OPERADORES
# =============================================================================

# Los operadores son símbolos que realizan operaciones sobre uno o más valores.

# --- 9.1 Operadores de comparación (devuelven True o False) ---
print(7 == 7)  # True  -> igual a
print(7 != 7)  # False -> distinto de
print(7 > 7)   # False -> mayor que
print(7 < 7)   # False -> menor que
print(7 >= 7)  # True  -> mayor o igual que
print(7 <= 7)  # True  -> menor o igual que

# --- 9.2 Operadores de pertenencia: `in` y `not in` ---
# Comprueban si un valor está (o no) dentro de una secuencia
# (lista, tupla, string...).

# En un string (distingue mayúsculas de minúsculas):
nombre = "Nacho"
print("N" in nombre)      # True
print("n" in nombre)      # False
print("a" not in nombre)  # False -> "a" sí está en "Nacho"

# En una lista:
frutas = ["manzana", "pera", "plátano", "naranja"]
print("manzana" in frutas)      # True
print("kiwi" in frutas)         # False
print("kiwi" not in frutas)     # True

# --- 9.3 Operadores de asignación ---
# Asignan un valor a una variable; los compuestos operan y asignan a la vez.
a = 5

a += 3  # equivale a: a = a + 3
print(a)  # 8

a -= 2  # equivale a: a = a - 2
print(a)  # 6

a *= 4  # equivale a: a = a * 4
print(a)  # 24

a /= 2  # equivale a: a = a / 2 (la división siempre devuelve float)
print(a)  # 12.0


# =============================================================================
# 10. CONDICIONALES
# =============================================================================

# Los condicionales ejecutan un bloque de código u otro según se cumpla una
# condición. Se escriben con `if`, `elif` y `else`.

# --- if / else con una comparación ---
age = 18

if age >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")

# --- if / else con un booleano ---
culpable = True

if culpable:
    print("Eres culpable")
else:
    print("Eres inocente")

# --- Comprobar si un número es par (resto de dividir entre 2 igual a 0) ---
x = 10

if x % 2 == 0:
    print("x es par")
else:
    print("x es impar")

# --- if / elif / else con un diccionario ---
# Se evalúan las condiciones en orden y se ejecuta solo la primera que se cumpla.
person = {
    "age": 17,
    "sonOfBoss": True,
}

if person["age"] >= 18:
    print("Eres mayor de edad")
elif person["sonOfBoss"]:
    print("Eres hijo del jefe")
else:
    print("Eres menor de edad y no eres hijo del jefe")
