# ==========================================
# CADENAS DE TEXTO - str
# ==========================================
# Una cadena representa texto.
#
# Se puede escribir utilizando:
# "comillas dobles"
# 'comillas simples'

nombre = "Carlos"
ciudad = 'San Salvador'

print(nombre)
print(ciudad)


# ------------------------------------------
# Saber el tipo
# ------------------------------------------

print(type(nombre))


# ------------------------------------------
# Concatenar textos
# ------------------------------------------

nombre = "Carlos"
apellido = "Martínez"

nombre_completo = nombre + " " + apellido

print(nombre_completo)


# ------------------------------------------
# f-strings
# ------------------------------------------

edad = 20

mensaje = f"Mi nombre es {nombre} y tengo {edad} años."

print(mensaje)


# ------------------------------------------
# Longitud
# ------------------------------------------

texto = "Python"

print(len(texto))


# ------------------------------------------
# Acceder a caracteres
# ------------------------------------------

palabra = "Python"

print(palabra[0])
print(palabra[1])
print(palabra[5])


# ------------------------------------------
# Métodos básicos
# ------------------------------------------

texto = "hola mundo"

print(texto.upper())
print(texto.lower())
print(texto.title())


# ------------------------------------------
# Reemplazar texto
# ------------------------------------------

mensaje = "Me gusta Java"

mensaje = mensaje.replace("Java", "Python")

print(mensaje)


# ==========================================
# EJERCICIO
# ==========================================

# Crea las variables:
#
# nombre
# apellido
# edad
# ciudad
#
# Después crea una frase utilizando
# f-strings.
