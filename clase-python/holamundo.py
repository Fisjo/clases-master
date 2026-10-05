
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

