==========================================
EJERCICIO PRÁCTICO - BOOLEANOS
==========================================
Pedimos el nombre al usuario
nombre = input("¿Cuál es tu nombre? ")

Pedimos la edad
input() devuelve texto, por eso usamos int()
edad = int(input("¿Cuántos años tienes? "))

==========================================
PRIMER MENSAJE
==========================================
Comprobamos si la edad es menor de 18
if edad < 18:
print(f"{nombre}, eres menor de edad.")
else:
print(f"{nombre}, eres mayor de edad.")

==========================================
SEGUNDO MENSAJE
==========================================
Comparamos si la edad es exactamente 18
es_mayor_de_18 = edad == 18

print(f"¿Tu edad es exactamente 18? {es_mayor_de_18}")

==========================================
EJEMPLO
==========================================
Si el usuario escribe:
¿Cuál es tu nombre? Carlos
¿Cuántos años tienes? 18
El programa mostrará:
Carlos, eres mayor de edad.
¿Tu edad es exactamente 18? True
Si escribe:
¿Cuál es tu nombre? Ana
¿Cuántos años tienes? 16
El programa mostrará:
Ana, eres menor de edad.
¿Tu edad es exactamente 18? False
==========================================
¿QUÉ ESTAMOS APRENDIENDO?
==========================================
input() -> pedir información al usuario
int() -> convertir texto a número entero
< -> comprobar si es menor
== -> comprobar si es igual
if -> tomar una decisión
else -> alternativa
True -> verdadero
False -> falso