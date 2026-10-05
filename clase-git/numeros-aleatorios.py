import random


def generar_numero_aleatorio(inicio=0, fin=100):
    return random.randint(inicio, fin)


def generar_lista_aleatoria(cantidad, inicio=0, fin=100):
    return [random.randint(inicio, fin) for _ in range(cantidad)]


if __name__ == "__main__":
    print("Generador de números aleatorios")
    cantidad = int(input("¿Cuántos números quieres generar? "))
    inicio = int(input("Valor mínimo: "))
    fin = int(input("Valor máximo: "))

    numeros = generar_lista_aleatoria(cantidad, inicio, fin)
    print("Números generados:", numeros)
    print("Número aleatorio único:", generar_numero_aleatorio(inicio, fin))
