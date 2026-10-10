# ==========================================
# TUPLAS - tuple
# ==========================================
# Una tupla permite almacenar varios valores.
#
# Se utilizan paréntesis ().
#
# Una diferencia importante con las listas:
# las tuplas no se pueden modificar después
# de crearlas.

colores = ("rojo", "verde", "azul")

print(colores)


# ------------------------------------------
# Saber el tipo
# ------------------------------------------

print(type(colores))


# ------------------------------------------
# Acceder a elementos
# ------------------------------------------

print(colores[0])
print(colores[1])
print(colores[2])


# ------------------------------------------
# Cantidad de elementos
# ------------------------------------------

print(len(colores))


# ------------------------------------------
# Recorrer una tupla
# ------------------------------------------

for color in colores:
    print(color)


# ------------------------------------------
# Tupla con diferentes tipos
# ------------------------------------------

persona = ("Carlos", 20, 1.75, True)

print(persona)


# ==========================================
# IMPORTANTE
# ==========================================

# Esto funciona con una lista:
#
# lista = ["rojo", "verde"]
# lista[0] = "amarillo"
#
# Pero esto genera un error:
#
# tupla = ("rojo", "verde")
# tupla[0] = "amarillo"


# ==========================================
# EJERCICIO
# ==========================================

# Crea una tupla llamada meses.
#
# Agrega:
# enero
# febrero
# marzo
#
# Después imprime cada mes utilizando
# un ciclo for.
