print("Bienvenido al codigo de Creacion de Automatas TDEA")
print("Vamos a empezar definiendo los simbolos de entrada")


def validar_no_deterministico(estadosConTransicion):
    for estado, transiciones in estadosConTransicion.items():
        for simbolo, destinos in transiciones.items():
            if len(destinos) > 1:
                return True
    return False


simbolosDeEntrada = []

while True:
    print("Ingresa un simbolo de Entrada: ")
    estado = input()
    if estado in simbolosDeEntrada:
        print("Error el simbolo de entrada ya habia sido añadido")
    else:
        simbolosDeEntrada.append(estado)

    print("Deseas ingresar otro simbolo de entrada? SI/NO?")
    entrada = input()
    if entrada.upper() == "SI":
        continue
    elif entrada.upper() == "NO":
        break
    else:
        print("error al ingresar valor")

print("---------------------")

estados = []
while True:
    print("Ingresa un simbolo de estado: ")
    estado = input()
    if estado in estados:
        print("error el simbolo ya existe")
    else:
        estados.append(estado)

    print("Desea ingresar otro estado? SI/NO?")
    entrada = input()
    if entrada.upper() == "SI":
        continue
    elif entrada.upper() == "NO":
        break
    else:
        print("error al ingresar valor")

print("---------------")
estadosConTransicion = {}

for estado in estados:
    print(f"Definiendo transiciones para el estado {estado}")
    transiciones_estado = {}
    for simbolo in simbolosDeEntrada:
        destinos = []
        while True:
            print(f"Ingrese un estado destino desde {estado} con simbolo {simbolo}:")
            destino = input()
            if destino in destinos:
                print("Error la transicion ya existia")
            else:
                destinos.append(destino)

            print(f"Desea ingresar otra transicion para simbolo {simbolo}? SI/NO?:")
            entrada = input()
            if entrada.upper() == "SI":
                continue
            elif entrada.upper() == "NO":
                break
            else:
                print("error al ingresar valor")
        transiciones_estado[simbolo] = destinos
    estadosConTransicion[estado] = transiciones_estado


print("Transiciones creadas:")
for estado, transicion in estadosConTransicion.items():
    print(f"Estado: {estado}")
    for simbolo, destinos in transicion.items():
        print(f"Con {simbolo} -> {destinos}")

print("El automata es:")
if validar_no_deterministico(estadosConTransicion):
    print("El automata es No deterministico")
else:
    print("El automata es deterministico")
