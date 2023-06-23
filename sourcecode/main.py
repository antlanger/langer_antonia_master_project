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

    

    # Original
    measureTime("Start Original Dendrogram at ")
    #dendrogramData.append(algorithm.start_needleman_wunsch(languages, sentences, combinations, filename="original"))
    dendrogram_original = algorithm.start_needleman_wunsch(languages, sentences, combinations, filename="original")
    simpleCreatePlot(dendrogram_original, languages, "dendrogram_original")
    measureTime("End Original Dendrogram at ")

    functions = [nlp.wordNormalization, nlp.removeSpecialCharacter, nlp.removePunctuation, nlp.removeWhitespace]
    filenames = ["wordNormalization", "removedDiacritics", "removedPunctuation", "removedWhitespace"]
    nlp._ABBREVIATION = languageAbb
    
    i = 0
    for func in functions:
        sentences = func(sentences)
        combinations = replaceCombinations(languages, sentences, combinations)
        measureTime("Start Dendrogram " + filenames[i] + " at ")
        #dendrogramData.append(algorithm.start_needleman_wunsch(languages, sentences, combinations, filename=filenames[i]))
        dendrogram = algorithm.start_needleman_wunsch(languages, sentences, combinations, filename=filenames[i])
        simpleCreatePlot(dendrogram, languages, filenames[i])
        measureTime("End Dendrogram " + filenames[i] + " at ")
        i = i + 1

    #createPlot(dendrogramData, languages)


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
    i = 0
    for language in languages:
        combinations[language] = sentences[i]
        i = i + 1
    return combinations


# ----------------------------------- START ---------------------------------- #
if __name__ == '__main__':
    main()

