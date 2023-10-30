import sys
import itertools
import time

left, right = 0, 1
K, V, Producciones = [], [], []
letras = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "W", "X", "Y", "Z"]

def union(lst1, lst2):
    final_list = list(set().union(lst1, lst2))
    return final_list

def cargarGramatica(grammarPath):
	file = open(grammarPath).read()
	K = (file.split("Variables:\n")[0].replace("Terminals:\n","").replace("\n",""))
	V = (file.split("Variables:\n")[1].split("Producciones:\n")[0].replace("Variables:\n","").replace("\n",""))
	P = (file.split("Producciones:\n")[1])

	return limpiarAlfabeto(K), limpiarAlfabeto(V), limpiarProduccion(P)

def limpiarProduccion(expresion):
	result = []
	reglasOriginales = expresion.replace('\n','').split(';')
	
	for regla in reglasOriginales:
		leftSide = regla.split(' -> ')[0].replace(' ','')
		rightTerms = regla.split(' -> ')[1].split(' | ')
		for term in rightTerms:
			result.append( (leftSide, term.split(' ')) )
	return result

def limpiarAlfabeto(expresion):
	return expresion.replace('  ',' ').split(' ')

def eliminarObjetivo(target, productions):
	trash, erased = [],[]
	for production in productions:
		if target in production[right] and len(production[right]) == 1:
			trash.append(production[left])
		else:
			erased.append(production)
			
	return trash, erased
 
def crearDiccionario(productions, variables, terms):
	result = {}
	for production in productions:
		if production[left] in variables and production[right][0] in terms and len(production[right]) == 1:
			result[production[right][0]] = production[left]
	return result

def reescribir(target, production):
    result = []
    
    positions = [i for i, x in enumerate(production[right]) if x == target]
    for i in range(len(positions) + 1):
        for element in list(itertools.combinations(positions, i)):
            tadan = [production[right][i] for i in range(len(production[right])) if i not in element]
            if tadan != []:
                result.append((production[left], tadan))
    return result

def findUnitary(rule, variables):
    if rule[left] in variables and rule[right][0] in variables and len(rule[right]) == 1:
        return True
    return False

def findSimple(rule):
    if rule[left] in V and rule[right][0] in K and len(rule[right]) == 1:
        return True
    return False

for nonTerminal in V:
    if nonTerminal in letras:
        letras.remove(nonTerminal)

def addS0(productions, variables):
    variables.append('S0')
    return [('S0', [variables[0]])] + productions

def newTerminal(productions, variables):
    newProducciones = []
    
    dictionary = crearDiccionario(productions, variables, terms=K)
    for production in productions:
        
        if findSimple(production):
            
            newProducciones.append(production)
        else:
            for term in K:
                for index, value in enumerate(production[right]):
                    if term == value and not term in dictionary:
                        
                        dictionary[term] = letras.pop()
                        
                        V.append(dictionary[term])
                        newProducciones.append((dictionary[term], [term]))

                        production[right][index] = dictionary[term]
                    elif term == value:
                        production[right][index] = dictionary[term]
            newProducciones.append((production[left], production[right]))

    
    return newProducciones

def twoVariables(productions, variables):
    result = []
    for production in productions:
        k = len(production[right])
        if k <= 2:
            result.append(production)
        else:
            newVar = letras.pop(0)
            variables.append(newVar + '1')
            result.append(
                (production[left], [production[right][0]] + [newVar + '1']))
            for i in range(1, k - 2):
                var, var2 = newVar + str(i), newVar + str(i + 1)
                variables.append(var2)
                result.append((var, [production[right][i], var2]))
            result.append((newVar + str(k - 2), production[right][k - 2:k]))
    return result

def removeEProductions(productions):
    newSet = []
    outlaws, productions = eliminarObjetivo(
        target='e', productions=productions)
    
    for outlaw in outlaws:
        for production in productions + [e for e in newSet if e not in productions]:
            if outlaw in production[right]:
                newSet = newSet + \
                    [e for e in reescribir(
                        outlaw, production) if e not in newSet]
    
    return newSet + ([productions[i] for i in range(len(productions)) if productions[i] not in newSet])

def unit_routine(rules, variables):
    unitaries, result = [], []
    for aRule in rules:
        if findUnitary(aRule, variables):
            unitaries.append((aRule[left], aRule[right][0]))
        else:
            result.append(aRule)
    for uni in unitaries:
        for rule in rules:
            if uni[right] == rule[left] and uni[left] != rule[left]:
                result.append((uni[left], rule[right]))

    return result

def removeUnit(productions, variables):
    i = 0
    result = unit_routine(productions, variables)
    tmp = unit_routine(result, variables)
    while result != tmp and i < 1000:
        result = unit_routine(tmp, variables)
        tmp = unit_routine(result, variables)
        i += 1
    return result

class Arbol:
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []

    def __repr__(self):
        if self.children:
            return '%s(%s)' % (self.label, ', '.join(map(str, self.children)))
        else:
            return self.label

    def __str__(self):
        return self.__repr__()


def crearArbol(table, sentence, i, j, A):
    for rule in R[A]:
        if len(rule) == 1:
            if rule[0] == sentence[i]:
                return Arbol(A, [Arbol(rule[0])])
        else:
            B = rule[0]
            C = rule[1]
            for k in range(i, j):
                if B in table[i][k] and C in table[k+1][j]:
                    return Arbol(A, [crearArbol(table, sentence, i, k, B), crearArbol(table, sentence, k+1, j, C)])
    return None

def CYK(sentence, non_terminals, R):
    n = len(sentence)
    table = [[[] for i in range(n)] for j in range(n)]
    for i in range(n):
        for A in non_terminals:
            for rule in R[A]:
                if sentence[i] in rule:
                    table[i][i].append(A)
    for l in range(1, n):
        for i in range(n-l):
            j = i + l
            for k in range(i, j):
                for A in non_terminals:
                    for rule in R[A]:
                        if len(rule) == 2:
                            B = rule[0]
                            C = rule[1]
                            if B in table[i][k] and C in table[k+1][j]:
                                table[i][j].append(A)
    return table

def parseCYK(oracion, non_terminals, R):
    print("Oracion: " + oracion)
    start_time = time.time()

    w = oracion.split()
    table = CYK(w, non_terminals, R)
    if "S" in table[0][len(w)-1]:
        print("SÍ")
    else:
        print("NO")

    Arbol = crearArbol(table, w, 0, len(w)-1, "S")
    print(Arbol)

    elapsed_time = time.time() - start_time
    print("Tiempo transcurrido: {:.10f} segundos".format(elapsed_time))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        grammarPath = str(sys.argv[1])
    else:
        grammarPath = 'gramatica.txt'

    K, V, Producciones = cargarGramatica(grammarPath)

    Producciones = addS0(Producciones, variables=V)
    Producciones = newTerminal(Producciones, variables=V)
    Producciones = twoVariables(Producciones, variables=V)
    Producciones = removeEProductions(Producciones)
    Producciones = removeUnit(Producciones, variables=V)

    non_terminals = V
    terminals = K
    R = {}

    for production in Producciones:
        left_side = production[left]
        right_side = production[right]

        if left_side in R:
            R[left_side].append(right_side)
        else:
            R[left_side] = [right_side]

    print("Variables = " + str(non_terminals))
    print("Terminales = " + str(terminals))
    print("Reglas = " + str(R))

    R['S0'] = [['S']]

    while True:
        user_input = input("Ingrese una oracion o escriba 'salir' para terminar: ")
        user_input = user_input.lower()

        if user_input.lower() == 'salir':
            break  
        
        parseCYK(user_input, non_terminals, R)
        print("\n")

    print("Hasta pronto!")
