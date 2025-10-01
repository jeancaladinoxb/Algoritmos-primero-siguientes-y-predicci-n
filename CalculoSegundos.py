def leer_gramatica(nombre_archivo):
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
    primeros = {nt: set() for nt in reglas}

    def first_de_simbolo(simbolo):
        if not simbolo.isupper():
            return {simbolo}
        if simbolo == "ε":
            return {"ε"}
        return primeros[simbolo]

    def calcular(nt):
        for produccion in reglas[nt]:
            for indice, s in enumerate(produccion):
                conjunto = set()
                if not s.isupper():
                    conjunto.add(s)
                elif s == "ε":
                    conjunto.add("ε")
                else:
                    calcular(s)
                    conjunto |= primeros[s]
                primeros[nt] |= (conjunto - {"ε"})
                if "ε" not in conjunto:
                    break
                if indice == len(produccion) - 1:
                    primeros[nt].add("ε")

    cambio = True
    while cambio:
        cambio = False
        snapshot = {k: set(v) for k, v in primeros.items()}
        for nt in reglas:
            calcular(nt)
        if snapshot != primeros:
            cambio = True
    return primeros

def calcular_siguientes(reglas, primeros, simbolo_inicial):
    siguientes = {nt: set() for nt in reglas}
    siguientes[simbolo_inicial].add("$")

    cambio = True
    while cambio:
        cambio = False
        for A, producciones in reglas.items():
            for produccion in producciones:
                for i, B in enumerate(produccion):
                    if B.isupper():
                        resto = produccion[i+1:]
                        conjunto_beta = set()
                        if resto:
                            for j, s in enumerate(resto):
                                f = primeros[s] if s.isupper() else {s}
                                conjunto_beta |= (f - {"ε"})
                                if "ε" not in f:
                                    break
                                if j == len(resto) - 1 and "ε" in f:
                                    conjunto_beta.add("ε")
                            antes = len(siguientes[B])
                            siguientes[B] |= (conjunto_beta - {"ε"})
                            if len(siguientes[B]) != antes:
                                cambio = True

                            if "ε" in conjunto_beta:
                                antes = len(siguientes[B])
                                siguientes[B] |= siguientes[A]
                                if len(siguientes[B]) != antes:
                                    cambio = True
                        else:
                            antes = len(siguientes[B])
                            siguientes[B] |= siguientes[A]
                            if len(siguientes[B]) != antes:
                                cambio = True
    return siguientes

if __name__ == "__main__":
    archivo = "gramatica.txt"
    G = leer_gramatica(archivo)
    simbolo_inicial = list(G.keys())[0]
    primeros_conjuntos = calcular_primeros(G)
    siguientes_conjuntos = calcular_siguientes(G, primeros_conjuntos, simbolo_inicial)

    print("Conjuntos de siguientes:")
    for nt, conjunto in siguientes_conjuntos.items():
        print(f"Siguiente({nt}) = {conjunto}")