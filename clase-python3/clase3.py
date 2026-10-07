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


## BREAK and CONTINUE ##

# La instrucción `break` se utiliza para salir de un bucle antes de que termine su ejecución normal. Por otro lado, la instrucción `continue` se utiliza para saltar a la siguiente iteración del bucle, omitiendo el resto del código en la iteración actual.

numeros = range(1, 100)  # Rango de números del 1 al 99

for numero in numeros:
    if numero % 2 == 0:
        print(f"{numero} es un número par, se saltará esta iteración.")
        continue  # Salta los números pares
    print(f"{numero} es un número impar, su cuadrado es {numero ** 2}.")
print("Fin del bucle.")



numeros2 = range(1, 100)  # Rango de números del 1 al 99
print("Objetivo: encontrar el ultimo numero primo menor a 100")
for numero in numeros2:
    if numero < 2:
        continue  # Salta los números menores a 2, ya que no son primos
    es_primo = True
    for i in range(2, int(numero ** 0.5) + 1):
        if numero % i == 0:
            es_primo = False
            break  # Sale del bucle si encuentra un divisor
    if es_primo:
        ultimo_primo = numero
print(f"El último número primo menor a 100 es: {ultimo_primo}")


lista_edades = [15, 22, 17, 30, 65, 45, 70, 19]

for edad in lista_edades:
    if edad < 18: 
        continue  # Salta las edades menores a 18
    if edad >= 65:
        print(f"{edad} es mayor de 65, se detendrá el bucle.")
        break  # Sale del bucle si encuentra una edad mayor a 65
    print(f"{edad} es una edad válida para el bucle.")


numeros = [12, 15, 32, 42, 55, 75, 122, 132, 150, 180, 200]

for i in numeros: 
    if i > 150: 
        break
    if i % 5 == 0: 
        print(i)
