import string
    
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
    

def findUnitTransitions(index, productions, result):
    keyList = list(productions.keys())
    key = keyList[index]
    for value in productions[key]:
        if len(value) == 1 and value.isupper():
                result.append((key, value))  

    index += 1
    
    if index < len(keyList):
        findUnitTransitions(index, productions, result)

    return result

def deleteUnitTransitions(unitTransitions, productions):
    for transition in unitTransitions:
        key = transition[0]
        value = transition[1]
        for values in productions[key]:
            if values == value:
                productions[key].remove(values)
                for val in productions[value]:
                    if val not in productions[key]:
                        if val.isupper():
                            if len(val) != 1:
                                productions[key].append(val)
                        else:
                            productions[key].append(val)
    return productions

def find_unique_uppercase_key(productions):
    keys = set(productions.keys())
    for letter in string.ascii_uppercase:
        if letter not in keys:
            return letter
        
def findMoreThanTwoVariables(productions):
    new_productions = productions.copy()  # Copia del diccionario original para evitar modificarlo directamente
    for key, values in new_productions.items():
        for value in values:
            numberOfVariables = 0
            if len(value) <= 2:
                continue
            for i in range(len(value) - 1):
                if value[i].isupper() and value[i + 1].isupper():
                    numberOfVariables += 1
                    break
            if numberOfVariables != 0:
                moreThanTwo = {}
                moreThanTwo[find_unique_uppercase_key(productions)] = value[-2] + value[-1]
                new_productions = renameMoreThaTwoVariables(new_productions, moreThanTwo)
    
    return new_productions  # Devuelve el diccionario modificado

def renameMoreThaTwoVariables(productions, moreThanTwo):
    new_productions = productions.copy()  # Copia del diccionario original para evitar modificarlo directamente
    for key, newTransition in moreThanTwo.items():
        for values in new_productions.values():
            for value in values:
                if len(value) <= 2:
                    continue
                match = 0
                position = []
                for i in range(len(value) - 1):
                    if value[i] == newTransition[-2] and value[i + 1] == newTransition[-1]:
                        match += 1
                        position.extend([i, i + 1])
                if match != 0:
                    listValue = list(value)
                    listValue.pop(position[1])
                    listValue.pop(position[0])
                    listValue.append(key)
                    values[values.index(value)] = "".join(listValue)
    for key, value in moreThanTwo.items():
        new_productions[key] = [value]
    return findMoreThanTwoVariables(new_productions)  # Devuelve el diccionario modificado

def findNonTerminalWithTerminal(productions):
    for key, values in productions.items():
        for value in values:
            if len(value) < 2:
                continue
            else:
                for letter in value:
                    if letter.islower():
                        moreThanTwo = {}
                        moreThanTwo[find_unique_uppercase_key(productions)] = letter
                        productions = renameTerminals(productions, moreThanTwo)
    return productions

def renameTerminals(productions, moreThanTwo):
    new_productions = productions.copy()
    for key, newTransition in moreThanTwo.items():
        for values in new_productions.values():
            for value in values:
                if len(value) == 1:
                    continue
                for letter in value:
                    if letter == newTransition:
                        listValue = list(value)
                        index = listValue.index(letter)
                        listValue.pop(index)
                        listValue.insert(index, key)
                        values[values.index(value)] = "".join(listValue)
                        value = "".join(listValue)

    for key, value in moreThanTwo.items():
        new_productions[key] = [value]
    
    return findNonTerminalWithTerminal(new_productions)


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

    """productions = {
        "S": ["NP VP"],
        "VP": ["VP PP", "cooks", "drinks", "eats", "cuts"],
        "PP": ["P NP"],
        "NP": ["Det N", "he", "she"],
        "V": ["cooks", "drinks", "eats", "cuts"],
        "P": ["in", "with"],
        "N": ["cat", "dog", "beer", "cake", "juice", "meat", "soup", "fork", "knife", "oven", "spoon"],
        "Det": ["a", "the"]
    }"""

    
    productions = addNewInitialVariable(productions)
    productions = removeNullProductions(productions)

    resultado = findUnitTransitions(0, productions, [])
    productions = deleteUnitTransitions(resultado, productions)
    productions = findMoreThanTwoVariables(productions)
    print(productions)

    #el programa no debe tener palabras, solo letras para que lo siguiente funcione
    """productions = findNonTerminalWithTerminal(productions)
    print(productions)
    productions = findMoreThanTwoVariables(productions)
    print(productions)"""
    