def cargar_gramatica(nombre_archivo):
    reglas = {}
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            lado_izq, lado_der = linea.split("->")
            lado_izq = lado_izq.strip()
            producciones = [p.strip().split() for p in lado_der.split("|")]
            if lado_izq not in reglas:
                reglas[lado_izq] = []
            reglas[lado_izq].extend(producciones)
    return reglas

def obtener_primeros(reglas):
    primeros = {no_terminal: set() for no_terminal in reglas}

    def primera_secuencia(seq):
        res = set()
        for idx, s in enumerate(seq):
            if not s.isupper() and s != "ε":
                res.add(s)
                return res
            elif s == "ε":
                res.add("ε")
                return res
            else:
                res |= (primeros[s] - {"ε"})
                if "ε" not in primeros[s]:
                    return res
        res.add("ε")
        return res

    cambio = True
    while cambio:
        cambio = False
        for nt in reglas:
            tamaño_anterior = len(primeros[nt])
            for prod in reglas[nt]:
                primeros[nt] |= primera_secuencia(prod)
            if len(primeros[nt]) != tamaño_anterior:
                cambio = True
    return primeros

def obtener_siguientes(reglas, firsts, inicio):
    follows = {nt: set() for nt in reglas}
    follows[inicio].add("$")

    cambio = True
    while cambio:
        cambio = False
        for A, producciones in reglas.items():
            for prod in producciones:
                for i, B in enumerate(prod):
                    if B.isupper():
                        resto = prod[i+1:]
                        conjunto = set()
                        if resto:
                            for j, s in enumerate(resto):
                                f = firsts[s] if s.isupper() else {s}
                                conjunto |= (f - {"ε"})
                                if "ε" not in f:
                                    break
                                if j == len(resto) - 1 and "ε" in f:
                                    conjunto.add("ε")
                            anterior = len(follows[B])
                            follows[B] |= (conjunto - {"ε"})
                            if "ε" in conjunto:
                                follows[B] |= follows[A]
                            if len(follows[B]) != anterior:
                                cambio = True
                        else:
                            anterior = len(follows[B])
                            follows[B] |= follows[A]
                            if len(follows[B]) != anterior:
                                cambio = True
    return follows

def generar_tabla_predicciones(reglas, firsts, follows):
    tabla = {}
    for A, prods in reglas.items():
        for prod in prods:
            key = f"{A} -> {' '.join(prod)}"
            first_prod = set()
            for i, s in enumerate(prod):
                if not s.isupper() and s != "ε":
                    first_prod.add(s)
                    break
                elif s == "ε":
                    first_prod.add("ε")
                    break
                else:
                    first_prod |= (firsts[s] - {"ε"})
                    if "ε" not in firsts[s]:
                        break
                    if i == len(prod) - 1:
                        first_prod.add("ε")
            if "ε" in first_prod:
                tabla[key] = (first_prod - {"ε"}) | follows[A]
            else:
                tabla[key] = first_prod
    return tabla

if __name__ == "__main__":
    archivo = "gramatica.txt"
    G = cargar_gramatica(archivo)
    simbolo_inicial = list(G.keys())[0]
    primeros = obtener_primeros(G)
    siguientes = obtener_siguientes(G, primeros, simbolo_inicial)
    predicciones = generar_tabla_predicciones(G, primeros, siguientes)

    print("Conjuntos de predicción:")
    for prod, conjunto in predicciones.items():
        print(f"Select({prod}) = {conjunto}")
