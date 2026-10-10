# ==========================================
# NONE - NoneType
# ==========================================
# None representa la ausencia de un valor.
#
# No significa:
# 0
# ""
# False
#
# Significa que no tenemos ningún valor.

resultado = None

print(resultado)


# ------------------------------------------
# Saber el tipo
# ------------------------------------------

print(type(resultado))

# Resultado:
# <class 'NoneType'>


# ------------------------------------------
# Podemos cambiar None posteriormente
# ------------------------------------------

nombre = None

print(nombre)

nombre = "Carlos"

print(nombre)


# ------------------------------------------
# Comparar con None
# ------------------------------------------

usuario = None

if usuario is None:
    print("No hay usuario")


# ==========================================
# EJERCICIO
# ==========================================

# Crea una variable llamada:
#
# resultado = None
#
# Comprueba utilizando if si resultado
# es None.
