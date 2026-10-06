## SETS ##

# Los sets son colecciones de elementos únicos, es decir, no permiten duplicados. Se pueden crear utilizando llaves {} o la función set().

numeros = set()

numeros.add(1)
numeros.add(2)
numeros.add(2)  # No se agregará porque ya existe

## REPASO CLASE 1 ##

print(numeros)  # Salida: {1, 2}

persona = {
    "nombre": "Juan",
    "edad": 30,
    "hobbies": ["fútbol", "lectura", "viajar"],
    "contacto": {
        "email": "juan@example.com",
        "telefono": "123456789"
    }
}

print(persona["nombre"])  # Salida: Juan
print(persona["hobbies"][1])  # Salida: lectura
print(persona["contacto"]["email"]) # Salida: juan@example.com

contrasena = "mimamamemima"
longitud_minima = 8
longitud_maxima = 20

if len(contrasena) < longitud_minima:
    print("La contraseña es demasiado corta.")
elif len(contrasena) > longitud_maxima:
    print("La contraseña es demasiado larga.")
else:
    print("La contraseña tiene una longitud válida.")


## BUCLES ##

# Los bucles permiten ejecutar un bloque de código varias veces. En Python, los bucles más comunes son el bucle for y el bucle while.

for i in range(5):
    print(i)  # Salida: 0, 1, 2, 3, 4

personas = ["Juan", "María", "Pedro", "Nacho", "Lucía", "Sofía", "Carlos", "Ana", "Luis", "Marta"]

for persona in personas:
    print(persona)  # Salida: Juan, María, Pedro, Nacho, Lucía, Sofía, Carlos, Ana, Luis, Marta  

colores = ["rojo", "verde", "azul"]

for color in colores:
    print(color)  # Salida: rojo, verde, azul


contador = 7
while contador < 12:
    print(contador)  # Salida: 7, 8, 9, 10, 11
    contador += 1


contador = 5 
while contador > 0: 
    print(contador)
    contador -= 1
print("¡Despegue!")

num = 5

while num > 0: 
    sum = ""
    nuevo_num = num
    while nuevo_num > 0:
        sum  += f"{nuevo_num} "
        nuevo_num -= 1
    print(sum)
    num -= 1


numero = 150

while numero < 351:
    if numero % 5 == 0 and numero % 7 == 0: 
        print(numero)
    numero += 1


frase = "Python es divertido"
i = 0

while i < len(frase):
    print(f"Índice: {i}, Letra: {frase[i]}")
    if frase[i] == " ":
        print(f"¡Espacio encontrado!")
    i += 1


## FUNCIONES ##

# Las funciones son bloques de código reutilizables que realizan una tarea específica. Se definen utilizando la palabra clave def.

def saludar(nombre):
    print(f"Hola, {nombre}!")

saludar("Juan")  # Salida: Hola, Juan!

def sumar(a, b):
    return a + b

print(sumar(3, 5))  # Salida: 8

def raiz_cuadrada(numero):
    if numero < 0:
        return "No se puede calcular la raíz cuadrada de un número negativo."
    else:
        return numero ** 0.5
    
print(raiz_cuadrada(15))  # Salida: 3.872983346207417
print(raiz_cuadrada(-4))  # Salida: No se puede calcular la raíz cuadrada de un número negativo.

## docstrings ##

def describir_persona(nombre, edad):
    """
    Esta función recibe el nombre y la edad de una persona y devuelve una descripción.
    
    Parámetros:
    nombre (str): El nombre de la persona.
    edad (int): La edad de la persona.
    
    Retorna:
    str: Una descripción de la persona.
    """
    return f"{nombre} tiene {edad} años."

print(describir_persona("Juan", 30))  # Salida: Juan tiene 30 años.
print(describir_persona.__doc__)  # Salida: Esta función recibe el nombre y la edad de una persona y devuelve una descripción.


def resta(a, b):
    return a - b

print(resta(10, 5))  # Salida: 5

def area_rectangulo(base, altura):
    return base * altura

print(area_rectangulo(5, 3))  # Salida: 15

def area_cuadrado(lado):
    ''' retorna el lado * lado'''
    return lado * lado
    

def area_triangulo(base, altura):
    ''' retorna base * altura / 2'''
    return base * altura / 2

area_total = area_cuadrado(10) + 5 * area_triangulo(2, 4)

def presentarse(nombre, apellido, edad):
    return f"Hola, me llamo {nombre} {apellido} y tengo {edad} años."

print(presentarse("Juan", "Pérez", 30))  # Salida: Hola, me llamo Juan Pérez y tengo 30 años.

def calcular_promedio(numeros):
    total = 0
    # Completa el bucle y el return
    for i in numeros: 
        total += i
    return total / len(numeros)

calificaciones = [85, 90, 78, 92, 88]
print(calcular_promedio(calificaciones))  # Salida: 86.6

def cuenta_caracteres(cadena):
    contador = 0
    if type(cadena) != str:
        return "Error: El argumento debe ser una cadena de texto."
    for caracter in cadena:
        contador += 1
    return contador

print(cuenta_caracteres("Hola, mundo!"))  # Salida: 13

def ultimo_caracter(texto):
    if type(texto) != str:
        return "Debo ser ejecutada con un string"
    return texto[-1]

texto = "Python"
print(ultimo_caracter(texto))  # Salida: n

def comparar(a, b):
    if a == b: 
        return "Son iguales"
    elif a > b: 
        return "El primero es mayor"
    else: 
        return "El segundo es mayor"

a = 10
b = 5
print(comparar(a, b))  # Salida: El primero es mayor

def contar_letra(texto, letra):
    count = 0
    texto = texto.upper()
    letra = letra.upper()
    for i in texto:
        if i == letra:
            count += 1
    return count

texto = "Hola, ¿cómo estás?"
letra = "o"
print(contar_letra(texto, letra))  # Salida: 2


def cuenta_atras(n):
    while n > 0:
        if n % 4 == 0: 
            print("Pum!")
        else:
            print(n)
        n -= 1
    print("¡Despegue!")

cuenta_atras(8)

def venta_online(pedido, fecha_entrega, incidencia=False):
    if incidencia == True: 
        return "Contacte con Att. Cliente"
    else: 
        return f"Su pedido {pedido} se entregará el {fecha_entrega}"
    
venta1 = venta_online("Libro de Python", "2024-07-15")
print(venta1)  # Salida: Su pedido Libro de Python se entregará el 2024-07-15

venta2 = venta_online("Libro de Python", "2024-07-15", incidencia=True)
print(venta2)  # Salida: Contacte con Att. Cliente

## FUNCIONES LAMBDA ##

# Las funciones lambda son funciones anónimas que se definen utilizando la palabra clave lambda. Se utilizan para crear funciones pequeñas y de una sola línea.

suma = lambda x, y: x + y
print(suma(3, 5))  # Salida: 8

resta = lambda x, y: x - y
print(resta(10, 5))  # Salida: 5

factorial = lambda n: 1 if n == 0 else n * factorial(n - 1)
print(factorial(5))  # Salida: 120

primera_letra = lambda palabra: palabra[0]
print(primera_letra("Python"))  # Salida: P

mas_diez = lambda a : a + 10
print(mas_diez(5))  # Salida: 15

doble = lambda a : 2 * a
print(doble(7))  # Salida: 14

