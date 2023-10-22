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
    
def countLetter(text, letter):
    count = 0
    for char in text:
        if char == letter:
            count += 1
    return count
                
    
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
                count = countLetter(values, val)
                for i in range(count):
                    if len(values) == 1:
                        productions[key].append("ε")
                    else:
                        if values.replace(val, "", i + 1) not in productions[key]:
                            productions[key].append(values.replace(val, "", i + 1))
    
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
    