# ==========================================
# CONVERSIÓN DE TIPOS DE DATOS
# ==========================================
# Python permite convertir un tipo de dato
# en otro utilizando funciones como:
#
# int()
# float()
# str()
# bool()


# ==========================================
# STR -> INT
# ==========================================

numero_texto = "25"

numero = int(numero_texto)

print(numero)
print(type(numero))


# ==========================================
# STR -> FLOAT
# ==========================================

precio_texto = "19.99"

precio = float(precio_texto)

print(precio)
print(type(precio))


# ==========================================
# INT -> STR
# ==========================================

edad = 20

edad_texto = str(edad)

print(edad_texto)
print(type(edad_texto))


# ==========================================
# INT -> FLOAT
# ==========================================

numero = 10

decimal = float(numero)

print(decimal)
print(type(decimal))


# ==========================================
# FLOAT -> INT
# ==========================================

numero = 10.99

entero = int(numero)

print(entero)

# Resultado:
# 10
#
# Se elimina la parte decimal.


# ==========================================
# BOOLEANOS
# ==========================================

print(bool(1))
print(bool(0))

print(bool("Hola"))
print(bool(""))


# ==========================================
# EJEMPLO PRÁCTICO
# ==========================================

edad = input("Escribe tu edad: ")

# input() siempre devuelve texto.
# Por eso debemos convertirlo a int.

edad = int(edad)

print("Tu edad es:", edad)

print(type(edad))


# ==========================================
# EJERCICIO
# ==========================================

# Pide al usuario:
#
# 1. Su nombre
# 2. Su edad
# 3. Su altura
#
# Convierte la edad a int
# y la altura a float.
#
# Después imprime los datos y sus tipos.
