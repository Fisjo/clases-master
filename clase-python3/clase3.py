## INPUTS ##

# Un imput es una función que permite al usuario ingresar datos desde la consola. En Python, se utiliza la función `input()` para capturar la entrada del usuario.

nombre = input("Por favor, ingresa tu nombre: ")
print(f"Hola, {nombre}! Bienvenido/a a la clase de Python.")

edad = int(input("Por favor, ingresa tu edad: "))
print(f"Tienes {edad} años.")

numero1 = float(input("Ingresa un número decimal: "))
numero2 = float(input("Ingresa otro número decimal: "))
suma = numero1 + numero2
print(f"La suma de {numero1} y {numero2} es: {suma}")

## CASTING ##

# El casting es el proceso de convertir un tipo de dato a otro. En Python, se puede realizar casting utilizando funciones como `int()`, `float()`, `str()`, etc.

print(int("123"))  # Convierte la cadena "123" a un entero
print(float("123.45"))  # Convierte la cadena "123.45" a un número decimal
print(str(123))  # Convierte el entero 123 a una cadena

## ROUND ##

# La función `round()` se utiliza para redondear un número decimal a un número específico de decimales.
# Con el 0.5, Python redondea al número par más cercano (redondeo bancario).

print(round(3.14159, 2))  # Redondea 3.14159 a 2 decimales
print(round(2.71828))  # Redondea 2.71828 al entero más cercano
print(round(2.5))  # Redondea 2.5 al entero más cercano (redondeo bancario)
print(round(3.5))  # Redondea 3.5 al entero más cercano (redondeo bancario)


