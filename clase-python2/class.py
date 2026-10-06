## SETS ##

# Los sets son colecciones de elementos únicos, es decir, no permiten duplicados. Se pueden crear utilizando llaves {} o la función set().

numeros = set()

numeros.add(1)
numeros.add(2)
numeros.add(2)  # No se agregará porque ya existe

print(numeros)  # Salida: {1, 2}

