==========================================
TYPE() EN PYTHON
==========================================
La función type() nos permite saber
qué tipo de dato contiene una variable.
Sintaxis:
type(variable)
==========================================
1. STRING - str
==========================================

nombre = "Carlos"

print(nombre)
print(type(nombre))

==========================================
2. ENTERO - int
==========================================

edad = 20

print(edad)
print(type(edad))

==========================================
3. DECIMAL - float
==========================================

altura = 1.75

print(altura)
print(type(altura))

==========================================
4. BOOLEANO - bool
==========================================

es_estudiante = True

print(es_estudiante)
print(type(es_estudiante))

==========================================
5. LISTA - list
==========================================

frutas = ["manzana", "banana", "naranja"]

print(frutas)
print(type(frutas))

==========================================
6. TUPLA - tuple
==========================================

colores = ("rojo", "verde", "azul")

print(colores)
print(type(colores))

==========================================
7. CONJUNTO - set
==========================================

numeros = {1, 2, 3, 4}

print(numeros)
print(type(numeros))

==========================================
8. DICCIONARIO - dict
==========================================

persona = {
"nombre": "Carlos",
"edad": 20
}

print(persona)
print(type(persona))

==========================================
9. NONE - NoneType
==========================================

resultado = None

print(resultado)
print(type(resultado))

==========================================
10. NÚMERO COMPLEJO - complex
==========================================

numero = 3 + 2j

print(numero)
print(type(numero))

==========================================
EJERCICIO 1
==========================================
Crea las siguientes variables:

nombre = "Ana"
edad = 25
altura = 1.65
es_estudiante = True

Muestra el tipo de cada variable.

print(type(nombre))
print(type(edad))
print(type(altura))
print(type(es_estudiante))

==========================================
EJERCICIO 2
==========================================
Pide datos al usuario.

nombre_usuario = input("Escribe tu nombre: ")
edad_usuario = int(input("Escribe tu edad: "))

Muestra los valores.

print("Nombre:", nombre_usuario)
print("Edad:", edad_usuario)

Muestra sus tipos.

print("Tipo del nombre:", type(nombre_usuario))
print("Tipo de la edad:", type(edad_usuario))

==========================================
EJERCICIO 3
==========================================
¿Qué tipo de dato tiene cada variable?

dato1 = "Python"
dato2 = 100
dato3 = 10.5
dato4 = False
dato5 = [1, 2, 3]
dato6 = (1, 2, 3)
dato7 = {1, 2, 3}
dato8 = {"nombre": "Ana"}
dato9 = None

print(type(dato1))
print(type(dato2))
print(type(dato3))
print(type(dato4))
print(type(dato5))
print(type(dato6))
print(type(dato7))
print(type(dato8))
print(type(dato9))

==========================================
EJERCICIO FINAL
==========================================
Pide al usuario:
Nombre
Edad
Altura
Después muestra:
El valor introducido
El tipo de dato

nombre = input("¿Cuál es tu nombre? ")
edad = int(input("¿Cuál es tu edad? "))
altura = float(input("¿Cuál es tu altura? "))

print()
print("========== RESULTADO ==========")

print("Nombre:", nombre)
print("Tipo:", type(nombre))

print("Edad:", edad)
print("Tipo:", type(edad))

print("Altura:", altura)
print("Tipo:", type(altura))ñ