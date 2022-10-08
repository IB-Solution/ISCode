#Module de traduction

import LanguagesPathFinder
import json
import re

# import sys
# _, argInFile, argOutFile, argFileSourceLang, argTargetLang = sys.argv   #Get the arguments

"""
    Traducteur d'un langage a un autre
"""

def ISCode(filePath: str, endID: int) -> None:
    """
        Param:
            filePath : Chemin vers le fichier à traduire
            endID : ID du langage final
    """
    startID: int = __GetLanguageID(filePath)                                        # ID du langage de départ
    languagePath: list[int] = LanguagesPathFinder.GetPath(startID, endID)           # Chemin vers le langage final

    instructions = open(filePath, 'r').readlines()                                  # Liste des instructions du fichier
    for xInstruction in range(len(instructions)): instructions[xInstruction] = instructions[xInstruction].replace('\n', '') # Suppression des sauts de ligne
        
    for xLanguage in range(1, len(languagePath)):                                   # Pour chaque langage du chemin
        #Si traduit
        instructions = __TranslateToLanguage(instructions, languagePath[xLanguage-1], languagePath[xLanguage])# Traduction des instructions  
        #Si compilé
    open(filePath.replace("."+str(startID), "."+str(endID)), 'w').write('\n'.join(instructions))# Enregistrement du fichier

    return


def __GetLanguageID(filePath: str) -> int:
    """
        Param:
            filePath : Chemin vers le fichier à traduire
        Return:
            ID du langage du fichier
    """
    return filePath.split('.')[-1]

def __GetLanguageData(languageID: int) -> dict:
    """
        Param:
            languageID : ID du langage
        Return:
            Dictionnaire des données du langage
    """
    return json.load(open(f'languages/{languageID}', 'r'))

def __Tokenize(lines: list[str], languageData: dict, nextLanguageID: int) -> list[dict[str, str, list[str]]]:
    """
        Décomposition des instructions en tokens
        Param:
            lines        : Liste des instructions du fichier
            languageData : Dictionnaire des données du langage
            nextLanguageID : ID du langage suivant
        Return:
            Liste des tokens {line:str, instruction:str, match:list[str]}
    """
    instructionList: list[dict[str, str, list[str]]] = []# Liste des ligne avec leur instruction {line: str, instruction: str}

    # Pour chaque lignes d'instructions, on liste les instructions du langage et on regarde si une instruction correspond a la ligne
    for line in lines:                                                              # Pour chaque instruction
        instructionFind: bool = False                                                   # Si une instruction a etait trouvé
        for languageInstruction in languageData["syntax"]['instruction'].keys():            # Pour chaque instruction du langage
            regex: str = ""                                                                     # Regex pour décomposer la ligne en Instruction
            for instructionToken in languageData["syntax"]['instruction'][languageInstruction]: # Pour chaque token present dans l'instruction actuel
                regex += "("+languageData["syntax"]["token"][instructionToken].replace("\\\\","\\")+")"# On ajoute le regex de l'instruction dans le regex de recheche (on remplace \\\\ en \\ pour que le regex soit correct car en json il faut mettre \\ or il faut \)
            #Lancer la recherche
            match = re.search(regex, line)                                           # On cherche si l'instruction correspond a une instruction du langage
            #Check si il y a match, arréter et mettre "instructionFind" a vrai
            if match != None:                                                                   # Si il y a match
                instructionFind = True                                                              # On indique que l'instruction a etait trouvé
                break                                                                               # On arrete la recherche pour cette instruction
        #Si trouvé
        if instructionFind:                                                                     # Si l'instruction a etait trouvé
            instructionList.append({"line": line, "instruction": languageInstruction, "match":match.groups()})# On ajoute l'instruction a la liste
        #Si pas trouvé
        else:                                                                                   # Si l'instruction n'a pas etait trouvé
            raise Exception(f"Instruction inconnue : {line}")                                       # On lance une erreur
    return instructionList

def __TranslateToLanguage(instructions: str, currentLanguageID: int, nextLanguageID: int) -> list[str]:
    """
        Param:
            instructions : Liste des instructions du fichier
            currentLanguageID : ID du langage actuel
            nextLanguageID : ID du langage suivant
        Return:
            Liste des instructions traduites
    """
    languageData: dict = __GetLanguageData(currentLanguageID)                       # Dictionnaire des données du langage

    # LEXER (tokenize)
    tokens: list[dict[str, str, list[str]]] = __Tokenize(instructions, languageData, nextLanguageID)     # Liste des tokens => [{line:str, instruction:str, match:list[str]}]

    # Translator
    newLines: list[str] = []                                                            # Liste des nouvelles instructions
    for token in tokens:                                                                # Pour chaque token
        newInstructions: str = languageData["output"][str(nextLanguageID)]["translationData"][token["instruction"]]# Nouvelle instruction
        for newInstruction in newInstructions:                                              # Pour chaque nouvelle instruction
            for xPart, part in enumerate(token["match"]):                                       # Pour chaque partie de l'instruction
                newInstruction = newInstruction.replace("%{"+str(xPart+1)+"}", part)                # On remplace les {} par les parties de l'instruction
            newLines.append(newInstruction)

    return newLines



if __name__ == '__main__':
    ISCode('test/helloWorld.1', 0)