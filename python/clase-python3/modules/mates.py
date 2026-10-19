def sumar(a, b):
    """Suma dos números."""
    return a + b

def restar(a, b):
    """Resta dos números."""
    return a - b

def multiplicar(a, b):
    """Multiplica dos números."""
    return a * b

def dividir(a, b):
    """Divide dos números, manejando la división por cero."""
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: No se puede dividir por cero.")
        
