# ==========================================
# BOOLEANOS - bool
# ==========================================
# Los booleanos representan dos posibilidades:
# True  = verdadero
# False = falso

# Crear variables booleanas
es_estudiante = True
tiene_trabajo = False

print(es_estudiante)
print(tiene_trabajo)

# ------------------------------------------
# Saber el tipo de dato
# ------------------------------------------

print(type(es_estudiante))

# Resultado:
# <class 'bool'>


# ------------------------------------------
# Comparaciones
# ------------------------------------------

edad = 20

print(edad >= 18)  # True
print(edad < 18)   # False


# ------------------------------------------
# Operadores de comparación
# ------------------------------------------

print(10 == 10)  # Igual
print(10 != 5)   # Diferente
print(10 > 5)    # Mayor
print(10 < 5)    # Menor
print(10 >= 10)  # Mayor o igual
print(5 <= 10)   # Menor o igual


# ------------------------------------------
# Operadores lógicos
# ------------------------------------------

es_mayor = True
tiene_documento = True

print(es_mayor and tiene_documento)

print(es_mayor or tiene_documento)

print(not es_mayor)


# ==========================================
# EJERCICIO
# ==========================================

# Crea dos variables booleanas:
# tiene_celular
# tiene_internet
#
# Después imprime el resultado de:
# tiene_celular and tiene_internet
