import helpers.textprocessing as nlp
import copy
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
import os
from datetime import datetime


# ----------------------------------- MAIN ----------------------------------- #
def main():
    print('STARTING ALGORITHM...')
    
    sentences = [
        "Das ist das Leben!",
        "This is life!"
    ]

    combinations = {
        "Deutsch" : "Das ist das Leben!",
        "Englisch" : "This is life!"
    }

    languages = [
        "Deutsch",
        "Englisch"
    ]


# ------------------------------- NLP FUNCTIONS ------------------------------ #

    functions_Normalization = [nlp.wordNormalization]
    functions_Punctuation = [nlp.removePunctuation]
    functions_Diacritics = [nlp.removeSpecialCharacter]
    functions_Whitespaces = [nlp.removeWhitespace]



# ------------------------------ SINGLE NLP STEP ----------------------------- #
   
    # Normalization x Original
    

    # Remove Punctuation x Original   
    punctuationSentences, puntuationCombinations = executeNLPSteps(sentences, combinations, functions_Punctuation, languages, "removedPunctuation")
    print("------------------")
    print(punctuationSentences)
    print(puntuationCombinations)
    print("------------------")

    # Remove Diacritics x Original   
    diacriticsSentences, diacriticsCombinations = executeNLPSteps(sentences, combinations, functions_Diacritics, languages, "removedDiacritics")

    # Remove Whitspaces x Original
    whitespacesSentences, whitespacesCombinations = executeNLPSteps(sentences, combinations, functions_Whitespaces, languages, "removedWhitespaces")
    #whitespacesSentences, whitespacesCombinations = executeNLPSteps(sentences, combinations, functions_Whitespaces, languages, "removedWhitespaces")

    print("------------------")
    print(punctuationSentences)
    print(puntuationCombinations)
    print("------------------")



# --------------------------- REPLACE COMBINATIONS --------------------------- #
def replaceCombinations(languages, sentences, combinations):
    """
        Replace the corresponding text from the language with the modified text retrieved from the NLP step.
    """   
    modCombinations = copy.copy(combinations)

    i = 0
    for language in languages:
        modCombinations[language] = sentences[i]
        i = i + 1
    return modCombinations

def executeNLPSteps(sentences, combinations, functions, languages, filename):
    
    modifiedSentences = functions[0](sentences)
    modifiedCombinations = replaceCombinations(languages, modifiedSentences, combinations)

    return modifiedSentences,modifiedCombinations


# ----------------------------------- START ---------------------------------- #
if __name__ == '__main__':
    main()

