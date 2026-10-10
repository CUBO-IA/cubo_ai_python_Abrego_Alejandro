# ==========================================
# DICCIONARIOS - dict
# ==========================================
# Un diccionario almacena información mediante
# una relación:
#
# clave -> valor
#
# Se utilizan llaves {}.

persona = {
    "nombre": "Carlos",
    "edad": 20,
    "ciudad": "San Salvador"
}

print(persona)


# ------------------------------------------
# Saber el tipo
# ------------------------------------------

print(type(persona))


# ------------------------------------------
# Acceder a valores
# ------------------------------------------

print(persona["nombre"])
print(persona["edad"])
print(persona["ciudad"])


# ------------------------------------------
# Agregar información
# ------------------------------------------

persona["profesion"] = "Programador"

print(persona)


# ------------------------------------------
# Modificar información
# ------------------------------------------

persona["edad"] = 21

print(persona)


# ------------------------------------------
# Eliminar información
# ------------------------------------------

del persona["profesion"]

print(persona)


# ------------------------------------------
# Obtener las claves
# ------------------------------------------

print(persona.keys())


# ------------------------------------------
# Obtener los valores
# ------------------------------------------

print(persona.values())


# ------------------------------------------
# Recorrer un diccionario
# ------------------------------------------

for clave, valor in persona.items():
    print(clave, ":", valor)


# ==========================================
# EJERCICIO
# ==========================================

# Crea un diccionario llamado estudiante.
#
# Debe contener:
#
# nombre
# edad
# carrera
# nota
#
# Después imprime cada dato.
