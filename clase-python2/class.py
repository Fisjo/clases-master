## SETS ##

# Los sets son colecciones de elementos únicos, es decir, no permiten duplicados. Se pueden crear utilizando llaves {} o la función set().

numeros = set()

numeros.add(1)
numeros.add(2)
numeros.add(2)  # No se agregará porque ya existe

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