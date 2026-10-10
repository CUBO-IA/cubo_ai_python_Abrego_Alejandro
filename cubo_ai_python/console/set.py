# ==========================================
# CONJUNTOS - set
# ==========================================
# Un set permite almacenar elementos únicos.
#
# Se utilizan llaves {}.

numeros = {1, 2, 3, 4, 5}

print(numeros)


# ------------------------------------------
# Saber el tipo
# ------------------------------------------

print(type(numeros))


# ------------------------------------------
# Los elementos repetidos desaparecen
# ------------------------------------------

numeros = {1, 2, 2, 3, 3, 4}

print(numeros)

# Resultado:
# {1, 2, 3, 4}


# ------------------------------------------
# Agregar elementos
# ------------------------------------------

numeros.add(5)

print(numeros)


# ------------------------------------------
# Eliminar elementos
# ------------------------------------------

numeros.remove(3)

print(numeros)


# ------------------------------------------
# Comprobar si existe un elemento
# ------------------------------------------

print(2 in numeros)
print(10 in numeros)


# ------------------------------------------
# Operaciones entre conjuntos
# ------------------------------------------

a = {1, 2, 3}
b = {3, 4, 5}

# Unión
print(a | b)

# Intersección
print(a & b)

# Diferencia
print(a - b)


# ==========================================
# EJERCICIO
# ==========================================

# Crea dos conjuntos:
#
# conjunto1 = {1, 2, 3, 4}
# conjunto2 = {3, 4, 5, 6}
#
# Imprime:
# 1. La unión
# 2. La intersección
# 3. La diferencia
