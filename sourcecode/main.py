import webscraper.Webscraper as webscraper
import needleman_wunsch.NeedlemanWunsch_01 as algorithm
import helpers.textprocessing as nlp

import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
import os

# ----------------------------------- MAIN ----------------------------------- #
def main():
    print('STARTING ALGORITHM...')
    
    dendrogramData = []
    languages, languageAbb, sentences, combinations = webscraper.start_scraping()
    
    # Original
    dendrogramData.append(algorithm.start_needleman_wunsch(languages, sentences, combinations, filename="original"))

    functions = [nlp.wordNormalization, nlp.removeSpecialCharacter, nlp.removePunctuation, nlp.removeWhitespace]
    filenames = ["wordNormalization", "removedDiacritics", "removedPunctuation", "removedWhitespace"]
    nlp._ABBREVIATION = languageAbb
    
    i = 0
    for func in functions:
        sentences = func(sentences)
        combinations = replaceCombinations(languages, sentences, combinations)
        dendrogramData.append(algorithm.start_needleman_wunsch(languages, sentences, combinations, filename=filenames[i]))
        i = i + 1

    createPlot(dendrogramData, languages)


# ------------------------------- PLOT CREATION ------------------------------ #
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

