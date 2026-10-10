# ==========================================
# LISTAS - list
# ==========================================
# Una lista permite almacenar varios valores.
#
# Las listas utilizan corchetes [].

frutas = ["manzana", "banana", "naranja"]

print(frutas)


# ------------------------------------------
# Saber el tipo
# ------------------------------------------

print(type(frutas))


# ------------------------------------------
# Acceder a elementos
# ------------------------------------------

print(frutas[0])
print(frutas[1])
print(frutas[2])


# ------------------------------------------
# Cambiar un elemento
# ------------------------------------------

frutas[0] = "pera"

print(frutas)


# ------------------------------------------
# Agregar elementos
# ------------------------------------------

frutas.append("uva")

print(frutas)


# ------------------------------------------
# Eliminar elementos
# ------------------------------------------

frutas.remove("banana")

print(frutas)


# ------------------------------------------
# Cantidad de elementos
# ------------------------------------------

print(len(frutas))


# ------------------------------------------
# Recorrer una lista
# ------------------------------------------

for fruta in frutas:
    print(fruta)


# ------------------------------------------
# Lista con diferentes tipos
# ------------------------------------------

datos = ["Carlos", 20, 1.75, True]

print(datos)


# ==========================================
# EJERCICIO
# ==========================================

# Crea una lista llamada animales.
#
# Debe contener:
# perro
# gato
# conejo
#
# Después:
# 1. Imprime la lista.
# 2. Imprime el primer elemento.
# 3. Agrega otro animal.
# 4. Recorre la lista con un for.
