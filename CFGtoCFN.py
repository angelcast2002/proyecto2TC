import itertools as it


def main():
    print("Hello World!")
    
def addNewInitialVariable(productions):
    addS = False
    new_productions = {}
    
    for value in productions.values():
        for production in value:
            if "S" in production:
                addS = True
                break

    if addS:
        new_productions["S'"] = ["S"]

    new_productions.update(productions)
    
    return new_productions

"""def removeNullProductions(productions):
    transitiveNullProductions = []
    for key, value in productions.items():
        for production in value:
            if "ε" in production:
                if key not in transitiveNullProductions:
                    transitiveNullProductions.append(key)
                

                
    print(transitiveNullProductions)"""  

def combinationsRemoveLetter(text, letter):
    n = text.count(letter)
    result = set()

    # Agregar la cadena sin la letra
    result.add(text.replace(letter, ''))

    # Generar combinaciones de quitar la letra
    for i in range(1, n + 1):
        for combo in it.combinations(range(n), i):
            removed_text = text
            for j in combo:
                removed_text = removed_text[:removed_text.index(letter, j)] + removed_text[removed_text.index(letter, j) + 1:]
            result.add(removed_text)

    return result

def removeNullProductions(productions):
    KeysNullProductions = []
    for key, value in productions.items():
        for production in value:
            if production == "ε":
                productions[key].remove(production)
                KeysNullProductions.append(key)
    
    for val in KeysNullProductions:
        for key, value in productions.items():
            for values in value:
                count = values.count(val)
                if count == 0:
                    continue
                else:
                    if len(values) == 1:
                            productions[key].append("ε")
                    else:
                        """comb = combinationsRemoveLetter(values, val)
                        for i in comb:
                            if i != "" and i not in productions[key]:
                                productions[key].append(i)"""
                        
                    
    
    if KeysNullProductions != []:
        removeNullProductions(productions) 
        
    return productions                              
    

         


if __name__ == '__main__':

    """PuttingNonTerminals = True
    terminals = []
    while PuttingNonTerminals:
        print("Ingresa la variable no terminal: ")
        terminals.append(input())
        print("Seguir ingresando variables no terminales? (Y/N)")
        if input() == 'N':
            PuttingNonTerminals = False
    print(terminals)
    
    productions = {}
    for i in terminals:
        print ("Ingresa las productions para la variable no terminal: " + i + " separdas por |")
        print("Ejemplo: aS|bS|c")
        productions[i] = input().split("|")"""
        
    productions = {
    "S": ["ASA", "aB"],
    "A": ["B", "S"],
    "B": ["b", "ε"]
    }
    
    productions = addNewInitialVariable(productions)
    productions = removeNullProductions(productions)
    print(productions)
    
    #main()
    