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
def convertir_afnd_a_afd(
    simbolosDeEntrada, estado_inicial, estados_finales, estadosConTransicion
):
    estado_inicial_afd = frozenset([estado_inicial])
    estados_afd = [estado_inicial_afd]
    transiciones_afd = {}
    estados_finales_afd = set()
    cola = deque([estado_inicial_afd])
    error_presente = False

    while cola:
        estado_actual = cola.popleft()
        nombre_estado_actual = (
            ",".join(sorted(estado_actual)) if estado_actual else "Error"
        )
        transiciones_afd[nombre_estado_actual] = {}

        for simbolo in simbolosDeEntrada:
            nuevo_estado = set()
            for subestado in estado_actual:
                destinos = estadosConTransicion.get(subestado, {}).get(simbolo, [])
                nuevo_estado.update(destinos)

            if not nuevo_estado:
                nombre_nuevo_estado = "Error"
                error_presente = True
            else:
                nombre_nuevo_estado = ",".join(sorted(nuevo_estado))
                if frozenset(nuevo_estado) not in estados_afd:
                    estados_afd.append(frozenset(nuevo_estado))
                    cola.append(frozenset(nuevo_estado))

                if any(e in estados_finales for e in nuevo_estado):
                    estados_finales_afd.add(nombre_nuevo_estado)

            transiciones_afd[nombre_estado_actual][simbolo] = [nombre_nuevo_estado]

    if error_presente:
        transiciones_afd.setdefault(
            "Error", {simbolo: ["Error"] for simbolo in simbolosDeEntrada}
        )

    return (
        transiciones_afd,
        ",".join(sorted(estado_inicial_afd)),
        list(estados_finales_afd),
        error_presente,
    )


# ============================
# Graficar el diagrama
# ============================
def graficar_diagrama_burbuja(
    estadosConTransicion,
    estado_inicial,
    estados_finales,
    titulo="automata",
    error_presente=False,
):
    nombre_archivo = f"diagrama_{titulo}"
    archivo_salida = f"{nombre_archivo}.png"

    dot = Digraph(comment=f"Diagrama de Burbuja del Autómata {titulo}")
    dot.attr(rankdir="LR")
    dot.attr(
        "node", shape="circle", style="filled", fillcolor="lightblue", fontname="Arial"
    )

    estados_validos = set(estadosConTransicion.keys())
    if error_presente:
        estados_validos.add("Error")

    for estado in estados_validos:
        if estado in estados_finales:
            dot.node(estado, shape="doublecircle", fillcolor="lightgreen")
        elif estado == "Error":
            dot.node(estado, shape="circle", fillcolor="red")
        else:
            dot.node(estado)

    dot.node("", shape="point")
    dot.edge("", estado_inicial)

    for estado_origen, transiciones in estadosConTransicion.items():
        for simbolo, destinos in transiciones.items():
            for destino in destinos or (["Error"] if error_presente else []):
                dot.edge(estado_origen, destino, label=simbolo)

    output_path = dot.render(filename=nombre_archivo, format="png", cleanup=True)
    print(f"\n✅ Diagrama de burbuja generado: {output_path}")
    if os.name == "posix":
        subprocess.run(["open", output_path])
    elif os.name == "nt":
        os.startfile(output_path)


# ============================
# Evaluar si una cadena es aceptada por el autómata
# ============================
def evaluar_cadena(cadena, estado_inicial, estados_finales, transiciones):
    estado_actual = estado_inicial
    for simbolo in cadena:
        if simbolo not in transiciones.get(estado_actual, {}):
            return False
        estado_actual = transiciones[estado_actual][simbolo][0]

    return estado_actual in estados_finales


# ============================
# Recoger entradas del usuario
# ============================
def recoger_entrada(mensaje):
    entrada = input(mensaje).strip()
    return entrada if entrada else "Error"


simbolosDeEntrada = []
print("Bienvenido al código de Creación de Autómatas TDEA")
print("Vamos a empezar definiendo los símbolos de entrada")

while True:
    simbolo = recoger_entrada("Ingresa un símbolo de entrada: ")
    if simbolo not in simbolosDeEntrada:
        simbolosDeEntrada.append(simbolo)
    else:
        print("Error: el símbolo ya había sido añadido")
    if input("¿Deseas ingresar otro símbolo de entrada? SI/NO: ").upper() == "NO":
        break

estados = []
while True:
    estado = recoger_entrada("Ingresa un símbolo de estado: ")
    if estado not in estados:
        estados.append(estado)
    else:
        print("Error: el símbolo ya existe")
    if input("¿Deseas ingresar otro estado? SI/NO: ").upper() == "NO":
        break

estado_inicial = recoger_entrada("¿Cuál es el estado inicial?: ")
while estado_inicial not in estados:
    print("Error: Ese estado no existe. Intenta de nuevo.")
    estado_inicial = recoger_entrada("¿Cuál es el estado inicial?: ")

estados_finales = []
while True:
    estado_final = recoger_entrada("Ingresa un estado final: ")
    if estado_final in estados and estado_final not in estados_finales:
        estados_finales.append(estado_final)
    else:
        print("Error: Estado inválido o repetido.")
    if input("¿Deseas agregar otro estado final? SI/NO: ").upper() == "NO":
        break

estadosConTransicion = {}
error_presente = False
for estado in estados:
    print(f"Definiendo transiciones para el estado {estado}")
    transiciones_estado = {}
    for simbolo in simbolosDeEntrada:
        destinos = []
        while True:
            destino = recoger_entrada(
                f"Ingrese un estado destino desde {estado} con símbolo '{simbolo}': "
            )
            if destino == "Error":
                error_presente = True

            if destino in estados or destino == "Error":
                destinos.append(destino)

            if (
                input(
                    f"¿Deseas ingresar otra transición para el símbolo '{simbolo}'? SI/NO: "
                ).upper()
                == "NO"
            ):
                break
        transiciones_estado[simbolo] = destinos
    estadosConTransicion[estado] = transiciones_estado

print("\n✅ Autómata definido correctamente.")
graficar_diagrama_burbuja(
    estadosConTransicion,
    estado_inicial,
    estados_finales,
    titulo="afnd",
    error_presente=error_presente,
)

afd_transiciones, afd_estado_inicial, afd_estados_finales, error_presente = (
    convertir_afnd_a_afd(
        simbolosDeEntrada, estado_inicial, estados_finales, estadosConTransicion
    )
)
print("\n🔄 Conversión a AFD completada.")
graficar_diagrama_burbuja(
    afd_transiciones,
    afd_estado_inicial,
    afd_estados_finales,
    titulo="afd",
    error_presente=error_presente,
)

cadena_a_probar = recoger_entrada(
    "\n🔍 Ingresa una cadena para evaluar en el autómata: "
)
print(
    "\n✅ La cadena es **ACEPTADA**"
    if evaluar_cadena(
        cadena_a_probar, estado_inicial, estados_finales, estadosConTransicion
    )
    else "\n❌ La cadena es **RECHAZADA**"
)
