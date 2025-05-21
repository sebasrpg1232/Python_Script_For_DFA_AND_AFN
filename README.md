Equipo de trabajo de Compiladores e Intérpretes I Lunes-Miercoles 8:00-10:00 PM

Integrantes

Carlos Enrique Guillent Carruyo

Sebastian Hernandez Bustamente

Este proyecto busca completar los requerimientos solicitados en la prática No1 de la asignatura teniendo como requerimiento.

Implementar un programa que permita convertir un autómata finito no determinístico (AFND) en
autómata finito determinístico (AFD)

1. Se le pide al usuario que introduzca el autómata finito no determinístico la aplicación debe
   validar si el autómata que el usuario ingreso es no determinístico.
2. Una vez realizada la validación se debe realizar el diagrama de burbuja (pintarlo).

3) Convertir el autómata finito no determinístico en determinístico y realizar el diagrama de
   burbuja (pintarlo).

Como correr el proyecto.


Ejemplo funcional

Símbolos de entrada

[a,b]

Estados

q0,q1,q2

Estado inicial 

q0

Estados finales

q2

Transiciones

| Estado | Símbolo | Destinos |
| ------ | -------- | -------- |
| q0     | a        | q1, q2   |
| q0     | b        | q2       |
| q1     | a        | q2       |
| q1     | b        | q0       |
| q2     | a        | q2       |
| q2     | b        | q1       |
