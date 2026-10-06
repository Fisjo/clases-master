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

numeros = [1, 2, 3, 4]

for i, num in enumerate(numeros):
    numeros[i] = num * 2  # Multiplicamos cada elemento por 2 y lo sobrescribimos

print(numeros)  # Resultado: [2, 4, 6, 8]

numeros = [1, 2, 3, 4]

for i in range(len(numeros)):
    numeros[i] = numeros[i] + 10  # Sumamos 10 a cada elemento

print(numeros)  # Resultado: [11, 12, 13, 14]

numeros = [1, 2, 3, 4]
numeros = [num * 2 for num in numeros]  # Sobrescribe la variable 'numeros' entera

print(numeros)  # Resultado: [2, 4, 6, 8]
