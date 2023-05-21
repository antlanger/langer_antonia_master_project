import unidecode
import string
from simplemma import text_lemmatizer

_ABBREVIATION = []

def removeWhitespace(sentences):
    sentences = modifySentence(sentences, 'removeWhitespaces')
    return sentences

def removePunctuation(sentences):
    sentences = modifySentence(sentences, 'removePunctation')
    return sentences

def removeSpecialCharacter(sentences):
    sentences = modifySentence(sentences, 'removeDiacritics')
    return sentences

def wordNormalization(sentences):   
    sentences = modifySentence(sentences, 'normalizeSentence')
    return sentences
    


#def toLower():

def modifySentence(sentences, operation):
    for i in range(len(sentences)):
        if operation == 'removeWhitespaces':
            modifiedSentence = sentences[i].replace(' ', '')
        elif operation == 'removePunctation':
            modifiedSentence = sentences[i].translate(str.maketrans('', '', string.punctuation))
        elif operation == 'removeDiacritics':
            modifiedSentence = unidecode.unidecode(sentences[i])
        elif operation == 'normalizeSentence':
            modifiedSentence = text_lemmatizer(sentences[i], lang=_ABBREVIATION[i])
            modifiedSentence = ' '.join(modifiedSentence)
            print(modifiedSentence)
        else:
            print('Nothing to do!')

        sentences[i] = modifiedSentence
    return sentences

    