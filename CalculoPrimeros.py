def cargar_gramatica(nombre_archivo):
    reglas = {}
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            izquierda, derecha = linea.split("->")
            izquierda = izquierda.strip()
            producciones = [p.strip().split() for p in derecha.split("|")]
            if izquierda not in reglas:
                reglas[izquierda] = []
            reglas[izquierda].extend(producciones)
    return reglas

def calcular_primeros(reglas):
    primeros_dict = {no_terminal: set() for no_terminal in reglas}

    def primero_de(simbolo):
        # Caso terminal o epsilon
        if not simbolo.isupper() and simbolo != "ε":
            return {simbolo}
        if simbolo == "ε":
            return {"ε"}

        # Caso no terminal
        resultado = set()
        for produccion in reglas[simbolo]:
            for idx, s in enumerate(produccion):
                primer_s = primero_de(s)
                resultado |= (primer_s - {"ε"})
                if "ε" not in primer_s:
                    break
                if idx == len(produccion) - 1:
                    resultado.add("ε")
        return resultado

    cambio = True
    while cambio:
        cambio = False
        for nt in reglas:
            antes = len(primeros_dict[nt])
            primeros_dict[nt] |= primero_de(nt)
            if len(primeros_dict[nt]) != antes:
                cambio = True
    return primeros_dict

if __name__ == "__main__":
    archivo = "gramatica.txt"
    G = cargar_gramatica(archivo)
    primeros_conjuntos = calcular_primeros(G)

    print("Conjuntos de primeros:")
    for nt, conjunto in primeros_conjuntos.items():
        print(f"Primero({nt}) = {conjunto}")