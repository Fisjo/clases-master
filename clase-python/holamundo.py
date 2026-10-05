
#esto es un comentario
print("Hola mundo")

patata: str = "patata"
print(patata)

pais: str = "España"
ciudad: str = "Madrid"

print(f"Vivo en {ciudad}, {pais}")

nombre: str = "Nacho"
apellido: str = "Pinazo"
print(f"Mi nombre es {nombre} {apellido}")

nombre_completo: str = f"{nombre} {apellido} Orihuela"
print(f"Mi nombre completo es {nombre_completo}")
print(type(nombre_completo))

n: int = 5
print(type(n))

tengo_carnet: bool = True
print(type(tengo_carnet))

print(patata[1]) #imprime la letra a
print(len(patata)) #imprime 6, que es la longitud de la palabra patata
print(patata.upper()) #imprime PATATA
print(patata.lower()) #imprime patata
print(patata.replace("a", "o")) #imprime pototo
print(patata.split("a")) #imprime ['p', 't', 't', '']

print(nombre.upper()) #imprime NACHO
print(len(nombre)) #imprime 5, que es la longitud de la palabra Nacho
print(nombre[0]) #imprime la letra N
print(apellido[-1]) #imprime la letra o

persona = {
    "nombre": "Nacho",
    "apellido": "Pinazo",
    "edad": 30,
    "ciudad": "Madrid",
    "soltero": True
}
print(persona["nombre"]) #imprime Nacho
print(persona["edad"]) #imprime 30
print(persona["ciudad"]) #imprime Madrid
print(persona["soltero"]) #imprime True

nombre_diccionario = persona.get("nombre") #imprime Nacho
print(nombre_diccionario)


# listas
frutas = ["manzana", "pera", "plátano", "naranja"]
print(frutas[0]) #imprime manzana
print(frutas[1]) #imprime pera
print(frutas[2]) #imprime plátano
print(frutas[3]) #imprime naranja

print(len(frutas)) #imprime 4, que es la longitud de la lista frutas
print(frutas)
print(frutas[0:2]) #imprime ['manzana', 'pera']
print(frutas[1:]) #imprime ['pera', 'plátano', 'naranja']
print(frutas[:3]) #imprime ['manzana', 'pera', 'plátano']
print(frutas[-1]) #imprime naranja

frutas.append("kiwi") #añade kiwi al final de la lista
print(frutas) #imprime ['manzana', 'pera', 'plátano', 'kiwi']

frutas.insert(1, "sandía") #añade sandía en la posición 1
print(frutas) #imprime ['manzana', 'sandía', 'pera', 'plátano', 'kiwi']

frutas.remove("pera") #elimina pera de la lista
print(frutas) #imprime ['manzana', 'sandía', 'plátano', 'kiwi']

frutas.pop() #elimina el último elemento de la lista
print(frutas) #imprime ['manzana', 'sandía', 'plátano']

frutas.sort() #ordena la lista de frutas alfabéticamente
print(frutas) #imprime ['manzana', 'naranja', 'plátano', 'sandía']

frutas.reverse() #invierte el orden de la lista de frutas
print(frutas) #imprime ['sandía', 'plátano', 'naranja', 'manzana']

compras = ["leche", "huevos", "pan", "mantequilla"]
compras.append("frutas") #añade frutas al final de la lista
compras.insert(2, "verduras") #añade verduras en la posición 2
compras.pop() #elimina el último elemento de la lista
print(compras) #imprime ['leche', 'huevos', 'verduras', 'pan', 'mantequilla']

compras_ordenadas = sorted(compras) #crea una nueva lista con las compras ordenadas alfabéticamente
print(compras_ordenadas) #imprime ['leche', 'mantequilla', 'pan', 'verduras', 'huevos']

###### TUPLAS ######

# las tuplas son inmutables, es decir, no se pueden modificar una vez creadas

fecha_nacimiento: tuple = ("30", "06", "1993")
print(fecha_nacimiento[0]) #imprime 30
print(fecha_nacimiento[1]) #imprime 06
print(fecha_nacimiento[2]) #imprime 1993

### CONSTANTES ###

# Las constantes son variables que no cambian su valor a lo largo del programa. En Python, no existe una forma de declarar una constante, pero se suele utilizar la convención de escribir el nombre de la variable en mayúsculas para indicar que es una constante.    

PI: float = 3.14159
IVA: float = 0.21

