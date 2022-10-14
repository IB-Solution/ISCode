# Gestionnaires des librairies
# Telechargement des langages non connue ou des librairies

import os
import requests

HIBOUKSTORE_API = ""

def GetLanguage(languageID: int) -> int:
    """
        Param:
            languageID : ID du langage à telecharger
        Return:
            0 : Réussi
            1 : Non trouvé
            2 : Non connecté à internet
    """
    ### CODE POUR CHECK ET DL

    return 0