import numpy as np
import pylab
from scipy.cluster.hierarchy import linkage, dendrogram

# Declare values to calculate scores
gap_penalty = -1
match_award = 1
mismatch_penalty = -1

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

def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty

def needleman_wunsch(sequence_one, sequence_two):
    n = len(sequence_one)
    m = len(sequence_two)

    # Empty score matrix
    score = np.zeros((m+1, n+1))
    
    # Fill the first column
    for i in range(0, m+1):
        score[i][0] = gap_penalty * i
    
    # Fill the first row
    for j in range(0, n+1):
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

    while j > 0:
        alignment_one += sequence_one[j-1]
        alignment_two += '-'
        j -= 1
    while i > 0:
        alignment_one += '-'
        alignment_two += sequence_two[i-1]
        i -= 1

    alignment_one = alignment_one[::-1]
    alignment_two = alignment_two[::-1]
    
    return (score, alignment_one, alignment_two)

def scoring_matrix(languages):
    scoring_matrix = np.zeros((len(languages),len(languages)))

    i = 0
    for x in languages:
        j = 0
        for y in languages:
            print()
            M, alignment1, alignment2 = needleman_wunsch(combinations.get(x), combinations.get(y)) 
            print("----------------------------------------------------------------------")
            print("ALIGNMENT OF ----> " + combinations.get(x) + " AND " + combinations.get(y) + " <----")
            print(alignment1)
            print(alignment2)
            print("----------------------------------------------------------------------")
            scoring_matrix[i][j] = M[-1][-1]
            j = j + 1
        i = i + 1
 
    return scoring_matrix

def get_matrix_max(matrix):
 
    max_value = None
 
    for i in range(0, len(matrix[0])):
        for j in range(0, len(matrix[0])):
            if(max_value == None):
                max_value = matrix[i][j]
            if(matrix[i][j] >= max_value):
                max_value = matrix[i][j]
 
    return max_value

def scoring_distance_matrix(scoring_matrix):
 
    scoring_distance_matrix = np.zeros((len(scoring_matrix[0]), len(scoring_matrix[0])))
    maxR = get_matrix_max(scoring_matrix)
 
    for i in range(0, len(language)):
        for j in range(0, len(language)):
            scoring_distance_matrix[i][j] = abs(scoring_matrix[i][j] - maxR)
 
    return scoring_distance_matrix

scoring = scoring_matrix(language)
scoring_distance_matrix = scoring_distance_matrix(scoring)
average = linkage(scoring_distance_matrix, "average")
dendrogram(average, labels=language)
pylab.subplots_adjust(bottom=0.1, left=0.2, right=1.0, top=1.0)
pylab.savefig("dendro.jpg")