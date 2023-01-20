import numpy as np

def add_bases (x, y, m):
    matrix = m.tolist()
    matrix.insert(0, [" ",  " "]+list(y))
    for i in range(2, len(x) + 2):
        matrix[i] = [list(x)[i-2]] + matrix[i]
    matrix[1] = [" "] + matrix[1]
    return matrix
    
def print_matrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

def needleman_wunsch(sequence_one, sequence_two, match = 1, mismatch = 1, gap = 2):
    length_sequence_one = len(sequence_one)
    length_sequence_two = len(sequence_two)
    
    # Initialization process - forming the base matrix
    F = np.zeros((length_sequence_one + 1, length_sequence_two + 1))
    F[:,0] = np.linspace(0, -gap*length_sequence_one, length_sequence_one + 1)
    F[0,:] = np.linspace(0, -gap*length_sequence_two, length_sequence_two + 1)
    
    # Pointers to trace through an optimal aligment.
    P = np.zeros((length_sequence_one + 1, length_sequence_two + 1))
    P[:,0] = 3
    P[0,:] = 4

    t = np.zeros(3)
    for i in range(length_sequence_one):
        for j in range(length_sequence_two):
            # Iteration step: take the max (inserting gap in first sequence, inserting gap in second sequence, match or mutation)
            if sequence_one[i] == sequence_two[j]:
                t[0] = F[i,j] + match
            else:
                t[0] = F[i,j] - mismatch
                    
            # Inserting gap in first sequence
            t[1] = F[i,j+1] - gap
            # Inserting gap in second sequence
            t[2] = F[i+1,j] - gap
            tmax = np.max(t)
                    
            F[i+1,j+1] = tmax
            if t[0] == tmax:
                P[i+1,j+1] += 2
                        
            # Higher weights for inserting gaps rather than matches/mismatches
            if t[1] == tmax:
                P[i+1,j+1] += 3
            if t[2] == tmax:
                P[i+1,j+1] += 4
    
    i = length_sequence_one
    j = length_sequence_two
    rx = []
    ry = []
    
    tracer_matrix = np.zeros((length_sequence_one+1, length_sequence_two+1))
    while i > 0 or j > 0:
        tracer_matrix[i, j] = -1
        
        if P[i,j] in [2, 5, 6, 9]:
            rx.append(sequence_one[i-1])
            ry.append(sequence_two[j-1])
            
            i -= 1
            j -= 1
        
        # if there's a gap in the first sequence
        elif P[i,j] in [3, 7]:
            rx.append(sequence_one[i-1])
            ry.append('-')
            i -= 1
            
        # if there's a gap in the second sequence
        elif P[i,j] in [4]:
            rx.append('-')
            ry.append(sequence_two[j-1])
            j -= 1

    print("Pointer matrix:")
    pointer_matrix = add_bases(x, y, P)
    print_matrix(pointer_matrix)
    
    print()
    print("Tracer matrix:")
    tracer_matrix = add_bases(x, y, tracer_matrix)
    print_matrix(tracer_matrix)
    
    # Reverse the strings.
    print()
    print("Final result:")
    
    rx = ''.join(rx)[::-1]
    ry = ''.join(ry)[::-1]
    
    px = "Sequence 1: " + rx
    py = "Sequence 2: " + ry
    return ['\n'.join([px, py]), rx, ry]



np.random.seed(12)

# For random sequences (sequence alignment not optimal)
x = ['Hallo', 'Das', 'Ist', 'Ein', 'Test']
y = ['Mama', 'Bitte', 'Gib', 'Mir', 'Das', 'Tuch']

printseq, seq1, seq2 = needleman_wunsch(x,y)
print(printseq)