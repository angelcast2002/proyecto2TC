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
  

def combinationsRemoveLetter(text, letter, index, result, originalText):
    listText = list(text)
    
    temp = listText.copy()
    if listText[index] == letter:
        temp = listText.copy()
        temp.pop(index)
        if "".join(temp) not in result and "".join(temp) != "":
            result.append("".join(temp))
        index = 0
    else:
        index += 1
    
    if index >= len(temp):
        index = 1
        temp = originalText
        reverseCombinationRemoveLetter(temp, letter, index, result)
    else:
        combinationsRemoveLetter("".join(temp), letter, index, result, originalText)
    
    return result

def reverseCombinationRemoveLetter(text, letter, index, result):
    listText = list(text)
    
    temp = listText.copy()
    if listText[-index] == letter:
            temp = listText.copy()
            temp.pop(-index)
            if "".join(temp) not in result and "".join(temp) != "":
                result.append("".join(temp))
            index = 1
    else:
        index += 1
    text = "".join(temp)
    if index >= len(text):
        return result
    else:
        reverseCombinationRemoveLetter(text, letter, index, result)
    
    
            

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
                        comb = combinationsRemoveLetter(values, val, 0, [], values)
                        for i in comb:
                            if i not in productions[key]:
                                productions[key].append(i)
                        
                    
    
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
    
    print(combinationsRemoveLetter("AAA", "A", 0, [], "AAA"))
    #productions = addNewInitialVariable(productions)
    #productions = removeNullProductions(productions)
    print(productions)
    
    #main()
    