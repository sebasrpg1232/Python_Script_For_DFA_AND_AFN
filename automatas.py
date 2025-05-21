import os
from graphviz import Digraph
import subprocess
from collections import deque

# ============================
# Validar si el autómata es no determinista
# ============================
def validar_no_deterministico(estadosConTransicion):
    for estado, transiciones in estadosConTransicion.items():
        for simbolo, destinos in transiciones.items():
            if len(destinos) > 1:
                return True
    return False

# ============================
# Función para convertir un AFND a AFD
# ============================
def convertir_afnd_a_afd(simbolosDeEntrada, estado_inicial, estados_finales, estadosConTransicion):
    estado_inicial_afd = frozenset([estado_inicial])
    estados_afd = [estado_inicial_afd]
    transiciones_afd = {}
    estados_finales_afd = set()
    cola = deque([estado_inicial_afd])

    while cola:
        estado_actual = cola.popleft()
        nombre_estado_actual = ",".join(sorted(estado_actual))
        transiciones_afd[nombre_estado_actual] = {}

        for simbolo in simbolosDeEntrada:
            nuevo_estado = set()
            for subestado in estado_actual:
                destinos = estadosConTransicion.get(subestado, {}).get(simbolo, [])
                nuevo_estado.update(destinos)

            if nuevo_estado:
                nuevo_estado_frozen = frozenset(nuevo_estado)
                nombre_nuevo_estado = ",".join(sorted(nuevo_estado))
                transiciones_afd[nombre_estado_actual][simbolo] = [nombre_nuevo_estado]

                if nuevo_estado_frozen not in estados_afd:
                    estados_afd.append(nuevo_estado_frozen)
                    cola.append(nuevo_estado_frozen)

                if any(e in estados_finales for e in nuevo_estado):
                    estados_finales_afd.add(nombre_nuevo_estado)

    return transiciones_afd, ",".join(sorted(estado_inicial_afd)), list(estados_finales_afd)

# ============================
# Graficar el diagrama
# ============================
def graficar_diagrama_burbuja(estadosConTransicion, estado_inicial, estados_finales, titulo='automata'):
    nombre_archivo = f'diagrama_{titulo}'
    archivo_salida = f"{nombre_archivo}.png"

    if os.path.exists(archivo_salida):
        os.remove(archivo_salida)

    dot = Digraph(comment=f'Diagrama de Burbuja del Autómata {titulo}')
    dot.attr(rankdir='LR')
    dot.attr('node', shape='circle', style='filled', fillcolor='lightblue', fontname='Arial')

    for estado in estadosConTransicion:
        if estado in estados_finales:
            dot.node(estado, shape='doublecircle', fillcolor='lightgreen')
        else:
            dot.node(estado)

    dot.node('', shape='point')
    dot.edge('', estado_inicial)

    for estado_origen, transiciones in estadosConTransicion.items():
        for simbolo, destinos in transiciones.items():
            for destino in destinos:
                dot.edge(estado_origen, destino, label=simbolo)

    output_path = dot.render(filename=nombre_archivo, format='png', cleanup=True)
    print(f"\n✅ Diagrama de burbuja generado: {output_path}")
    if os.name == 'posix':
        subprocess.run(['open', output_path])
    elif os.name == 'nt':
        os.startfile(output_path)

# ============================
# Recoger entradas del usuario (como ya tienes)
# ============================
simbolosDeEntrada = []
print("Bienvenido al código de Creación de Autómatas TDEA")
print("Vamos a empezar definiendo los símbolos de entrada")

while True:
    simbolo = input("Ingresa un símbolo de entrada: ")
    if simbolo in simbolosDeEntrada:
        print("Error: el símbolo ya había sido añadido")
    else:
        simbolosDeEntrada.append(simbolo)
    if input("¿Deseas ingresar otro símbolo de entrada? SI/NO: ").upper() == "NO":
        break

estados = []
while True:
    estado = input("Ingresa un símbolo de estado: ")
    if estado not in estados:
        estados.append(estado)
    else:
        print("Error: el símbolo ya existe")
    if input("¿Deseas ingresar otro estado? SI/NO: ").upper() == "NO":
        break

estado_inicial = input("¿Cuál es el estado inicial?: ")
while estado_inicial not in estados:
    estado_inicial = input("Ese estado no existe. Intenta de nuevo: ")

estados_finales = []
while True:
    estado_final = input("Ingresa un estado final: ")
    if estado_final in estados and estado_final not in estados_finales:
        estados_finales.append(estado_final)
    else:
        print("Estado inválido o repetido.")
    if input("¿Deseas agregar otro estado final? SI/NO: ").upper() == "NO":
        break

estadosConTransicion = {}
for estado in estados:
    print(f"Definiendo transiciones para el estado {estado}")
    transiciones_estado = {}
    for simbolo in simbolosDeEntrada:
        destinos = []
        while True:
            destino = input(f"Ingrese un estado destino desde {estado} con símbolo '{simbolo}': ")
            if destino in estados and destino not in destinos:
                destinos.append(destino)
            else:
                print("Estado destino inválido o repetido")
            if input(f"¿Deseas ingresar otra transición para el símbolo '{simbolo}'? SI/NO: ").upper() == "NO":
                break
        transiciones_estado[simbolo] = destinos
    estadosConTransicion[estado] = transiciones_estado

# Mostrar transiciones
print("\nTransiciones creadas:")
for estado, transiciones in estadosConTransicion.items():
    print(f"{estado}: {transiciones}")

# Validar y graficar
if validar_no_deterministico(estadosConTransicion):
    print("\n🧠 El autómata es No determinista (AFND)")
else:
    print("\n✅ El autómata es determinista (AFD)")

# Graficar AFND original
graficar_diagrama_burbuja(estadosConTransicion, estado_inicial, estados_finales, titulo='afnd')

# Convertir a AFD y graficar
afd_transiciones, afd_estado_inicial, afd_estados_finales = convertir_afnd_a_afd(
    simbolosDeEntrada, estado_inicial, estados_finales, estadosConTransicion
)

print("\n🔄 Conversión a AFD completada.")
graficar_diagrama_burbuja(afd_transiciones, afd_estado_inicial, afd_estados_finales, titulo='afd')
