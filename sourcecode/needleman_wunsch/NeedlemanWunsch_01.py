import numpy as np
import os
from scipy.cluster import hierarchy
import codecs
from numba import prange, njit

# Declare values to calculate scores
gap_penalty = -1
match_award = 1
mismatch_penalty = -1

'''
language = [
    'Deutsch',
    'Englisch',
    'Französisch',
    'Spanisch',
    'Italienisch',
    'Finnisch'
]
 
sentences = [
    'Das ist das Leben',
    'This is life',
    'C\'est la vie',
    'Así es la vida',
    'Questa è vita',
    'Tämä on elämää'
]

combinations = {
    'Deutsch':'Das ist das Leben',
    'Englisch':'This is life',
    'Französisch':'C\'est la vie',
    'Spanisch':'Así es la vida',
    'Italienisch':'Questa è vita',
    'Finnisch':'Tämä on elämää'   
}
'''

@njit
def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty

@njit(parallel=True)
def needleman_wunsch(sequence_one, sequence_two):
    n = len(sequence_one)
    m = len(sequence_two)

    # Empty score matrix
    score = np.zeros((m+1, n+1))
    
    # Fill the first column
    for i in prange(0, m+1):
        score[i][0] = gap_penalty * i
    
    # Fill the first row
    for j in prange(0, n+1):
        score[0][j] = gap_penalty * j


    for k in range(1,m+1):
        for l in range(1, n+1):
            match = score[k - 1][l - 1] + match_score(sequence_one[l-1], sequence_two[k-1])
            delete = score[k - 1][l] + gap_penalty
            insert = score[k][l - 1] + gap_penalty

            score[k][l] = max(match, delete, insert)

    #print(score)
    

    # Traceback and alignment
    
    alignment_one = ""
    alignment_two = ""

    i = m
    j = n

    while i > 0 and j > 0:
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]

        # Check to figure out which cell the current score was calculated from,
        # then update i and j to correspond to that cell.
        if score_current == score_diagonal + match_score(sequence_one[j-1], sequence_two[i-1]):
            alignment_one += sequence_one[j-1]
            alignment_two += sequence_two[i-1]
            i -= 1
            j -= 1
        elif score_current == score_up + gap_penalty:
            alignment_one += sequence_one[j-1]
            alignment_two += '-'
            j -= 1
        elif score_current == score_left + gap_penalty:
            alignment_one += '-'
            alignment_two += sequence_two[i-1]
            i -= 1

    # Finish tracing up to the top left cell
    while j > 0:
        alignment_one += sequence_one[j-1]
        alignment_two += '-'
        j -= 1
    while i > 0:
        alignment_one += '-'
        alignment_two += sequence_two[i-1]
        i -= 1

    # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
    # These two lines reverse the order of the characters in each sequence.
    alignment_one = alignment_one[::-1]
    alignment_two = alignment_two[::-1]
    
    return (score, alignment_one, alignment_two)

def scoring_matrix(languages, sentences, combinations, filename, textLength):
    scoring_matrix = np.zeros((len(languages),len(languages)))


    i = 0
    f = codecs.open(os.path.abspath(os.curdir) + '/sourcecode/files/' + textLength + '/' + filename + ".txt", "w", encoding='utf-16')
    
    for x in languages:
        j = 0
        for y in languages:
            M, alignment1, alignment2 = needleman_wunsch(combinations.get(x), combinations.get(y))
            f.write('------------------------------')
            f.write("\n")
            f.write('Sentence 1: ' + combinations.get(x))
            f.write("\n")
            f.write('Sentence 2: ' + combinations.get(y))
            f.write("\n")
            f.write('Alignment:')
            f.write("\n")
            f.write(alignment1)
            f.write("\n")
            f.write(alignment2)
            f.write("\n")
            f.write('------------------------------')
            f.write("\n")
            scoring_matrix[i][j] = M[-1][-1]
            j = j + 1
        i = i + 1
    f.close()
    return scoring_matrix

@njit(parallel=True)
def get_matrix_max(matrix):
 
    max_value = -np.inf
 
    for i in range(0, len(matrix[0])):
        for j in range(0, len(matrix[0])):
            if(max_value == -np.inf):
                max_value = matrix[i][j]
            if(matrix[i][j] >= max_value):
                max_value = matrix[i][j]
 
    return max_value

@njit(parallel=True)
def scoring_distance_matrix(scoring_matrix, languages):
 
    scoring_distance_matrix = np.zeros((len(scoring_matrix[0]), len(scoring_matrix[0])))
    maxR = get_matrix_max(scoring_matrix)
 
    for i in range(0, len(languages)):
        for j in range(0, len(languages)):
            scoring_distance_matrix[i][j] = abs(scoring_matrix[i][j] - maxR)
 
    return scoring_distance_matrix


# ------------------------------- START METHOD ------------------------------- #
def start_needleman_wunsch(languages, sentences, combinations, filename="algorithm", textLength="null"):
    scoring = scoring_matrix(languages, sentences, combinations, filename, textLength)
    scoring_distance_matrix1 = scoring_distance_matrix(scoring, languages)
    
    f =  codecs.open(os.path.abspath(os.curdir) + '/sourcecode/files/' + textLength + '/' + filename + "_scoring_matrix" + ".txt", "w", encoding="utf-16")
    f.write(np.array2string(scoring))
    f.close()
    
    #print(scoring)
    average = hierarchy.linkage(scoring_distance_matrix1, "average")
    return average