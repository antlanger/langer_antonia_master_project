import webscraper.Webscraper as webscraper
import needleman_wunsch.NeedlemanWunsch_01 as algorithm
import helpers.textprocessing as nlp

import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
import os
from datetime import datetime

def measureTime(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(message, current_time)

# ----------------------------------- MAIN ----------------------------------- #
def main():
    print('STARTING ALGORITHM...')
    
    dendrogramData = []
    languages, languageAbb, sentences, combinations = webscraper.start_scraping()

    print(combinations)

    

    # Original
    measureTime("Start Original Dendrogram at ")
    #dendrogramData.append(algorithm.start_needleman_wunsch(languages, sentences, combinations, filename="original"))
    dendrogram_original = algorithm.start_needleman_wunsch(languages, sentences, combinations, filename="original")
    simpleCreatePlot(dendrogram_original, languages, "dendrogram_original")
    measureTime("End Original Dendrogram at ")

    #functions = [nlp.wordNormalization, nlp.removeSpecialCharacter, nlp.removePunctuation, nlp.removeWhitespace]
    #filenames = ["wordNormalization", "removedDiacritics", "removedPunctuation", "removedWhitespace"]
    nlp._ABBREVIATION = languageAbb


# ------------------------------- NLP FUNCTIONS ------------------------------ #

    functions_Normalization = [nlp.wordNormalization]
    functions_Punctuation = [nlp.removePunctuation]
    functions_Diacritics = [nlp.removeSpecialCharacter]
    functions_Whitespaces = [nlp.removeWhitespace]



# ------------------------------ SINGLE NLP STEP ----------------------------- #
   
    # Normalization x Original
    normalizedSentences, normalizedCombinations = executeNLPSteps(sentences, combinations, functions_Normalization, languages, "wordNormalization")

    # Remove Punctuation x Original   
    punctuationSentences, puntuationCombinations = executeNLPSteps(sentences, combinations, functions_Punctuation, languages, "removedPunctuation")

    # Remove Diacritics x Original   
    diacriticsSentences, diacriticsCombinations = executeNLPSteps(sentences, combinations, functions_Diacritics, languages, "removedDiacritics")

    # Remove Whitspaces x Original
    executeNLPSteps(sentences, combinations, functions_Whitespaces, languages, "removedWhitespaces")
    #whitespacesSentences, whitespacesCombinations = executeNLPSteps(sentences, combinations, functions_Whitespaces, languages, "removedWhitespaces")

# ------------------------------- TWO NLP STEPS ------------------------------ #

    # Normalization x RemovePunctuation
    normalization_punctuation_sentences, normalization_punctuation_combinations = executeNLPSteps(normalizedSentences, normalizedCombinations, functions_Punctuation, languages, "normalization_punctuation")

    # Normalization x RemoveDiacritics
    normalization_diacritics_sentences, normalization_diacritics_combinations = executeNLPSteps(normalizedSentences, normalizedCombinations, functions_Diacritics, languages, "normalization_diacritics")

    # Normalization x RemoveWhitespaces
    executeNLPSteps(normalizedSentences, normalizedCombinations, functions_Whitespaces, languages, "normalization_whitespaces")
    #normalization_whitespaces_sentences, normalization_whitespaces_combinations = executeNLPSteps(normalizedSentences, normalizedCombinations, functions_Whitespaces, languages, "normalization_whitespaces")

#--------------------------------------------------

    # Remove Punctuation x Remove Diacritics
    punctuation_diacritics_sentences, punctuation_diacritics_combinations = executeNLPSteps(punctuationSentences, puntuationCombinations, functions_Diacritics, languages, "punctuation_diacritics")

    # Remove Punctuation x Remove Whitespaces
    executeNLPSteps(punctuationSentences, puntuationCombinations, functions_Whitespaces, languages, "punctuation_whitespaces")

#--------------------------------------------------

    # Remove Diacritics x Remove Whitespaces
    executeNLPSteps(diacriticsSentences, diacriticsCombinations, functions_Whitespaces, languages, "diacritics_whitespaces")


# ------------------------------ THREE NPL STEPS ----------------------------- #

    # Normalization x Remove Punctuation x Remove Diacritics
    executeNLPSteps(normalization_punctuation_sentences, normalization_punctuation_combinations, functions_Diacritics, languages, "normalization_punctuation_diacritics")

    # Normalization x Remove Diacritics x Remove Whitespaces
    normalization_diacritics_whitespaces_sentences, normalization_diacritics_whitespaces_combinations = executeNLPSteps(normalization_diacritics_sentences, normalization_diacritics_combinations, functions_Whitespaces, languages, "normalization_diacritics_whitespaces")

    # Normalization x Remove Punctuation x Remove Whitespaces
    executeNLPSteps(normalization_punctuation_sentences, normalization_punctuation_combinations, functions_Whitespaces, languages, "normalization_punctuation_whitespaces")

    # Remove Punctuation x Remove Diacritics x Remove Whitespaces
    executeNLPSteps(punctuation_diacritics_sentences, punctuation_diacritics_combinations, functions_Whitespaces, languages, "punctuation_diacritics_whitespaces")

# ------------------------------ FOUR NLP STEPS ------------------------------ #

    # Normalization x Remove Diacritcs x Remove Whitespaces x Remove Punctuation
    executeNLPSteps(normalization_diacritics_whitespaces_sentences, normalization_diacritics_whitespaces_combinations, functions_Punctuation, languages, "allmethods")


# ------------------------------- PLOT CREATION ------------------------------ #

def simpleCreatePlot(data, languages, filename):
    plt.figure(figsize=(14,7))
    dn = hierarchy.dendrogram(data, labels=languages)
    plt.savefig(os.path.abspath(os.curdir) + '/sourcecode/files/' + filename +".jpg")

def createPlot(data, languages):
    fig, axes = plt.subplots(3, 2, figsize=(12, 8))
    #print(axes)
    
    #original
    dn1 = hierarchy.dendrogram(data[0],labels=languages, orientation='top', ax=axes[0][0])
    # without diacritics
    dn2= hierarchy.dendrogram(data[1], ax=axes[0][1],
                           orientation='top', labels=languages)
    # without punctuation
    dn3 = hierarchy.dendrogram(data[2], ax=axes[1][0],
                           orientation='top', labels=languages)
    # without whitespaces
    dn4 = hierarchy.dendrogram(data[3], ax=axes[1][1],
                           orientation='top', labels=languages)
    dn5 = hierarchy.dendrogram(data[4], ax=axes[2][0],
                           orientation='top', labels=languages)
    plt.savefig(os.path.abspath(os.curdir) + '/sourcecode/files/' + "dendrogramplt1.jpg")
    plt.show()


# --------------------------- REPLACE COMBINATIONS --------------------------- #
def replaceCombinations(languages, sentences, combinations):
    """
        Replace the corresponding text from the language with the modified text retrieved from the NLP step.
    """   
    
    i = 0
    for language in languages:
        combinations[language] = sentences[i]
        i = i + 1
    return combinations

def executeNLPSteps(sentences, combinations, functions, languages, filename):
    
    modifiedSentences = functions[0](sentences)
    modifiedCombinations = replaceCombinations(languages, modifiedSentences, combinations)

    measureTime("Start Dendrogram " + filename + " at ")
    dendrogram = algorithm.start_needleman_wunsch(languages, modifiedSentences, modifiedCombinations, filename=filename)
    simpleCreatePlot(dendrogram, languages, filename)
    measureTime("End Dendrogram " + filename + " at ")

    return modifiedSentences,modifiedCombinations


# ----------------------------------- START ---------------------------------- #
if __name__ == '__main__':
    main()

