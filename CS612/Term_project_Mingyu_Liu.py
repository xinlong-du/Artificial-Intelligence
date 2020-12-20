#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS612 Algorithms in Bioinformatics Term Project

@author: Mingyu Liu
"""
import numpy as np
from dsppkeras.datasets import dspp
from scipy.linalg import hankel
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# def convert_input(sequence):
#     aa_code = 'ACDEFGHIKLMNPQRSTVWY '
# # define a mapping of chars to integers
#     char_to_int = dict((c, i) for i, c in enumerate(aa_code))
# # integer encode input data
#     integer_encoded = [char_to_int[char] for char in sequence]
# # one hot encode
#     onehot_encoded = list()
#     for value in integer_encoded:
#         letter = [0 for _ in range(len(aa_code))]
#         letter[value] = 1
#         onehot_encoded.append(letter)
#     onehot_encoded = np.asarray(onehot_encoded)
#     return onehot_encoded

def convert_residue(residue):
    results = np.zeros(21)
    if residue == 'A':
        results[0] = 1
    elif residue == 'R':
        results[1] = 1
    elif residue == 'N':
        results[2] = 1
    elif residue == 'D':
        results[3] = 1
    elif residue == 'C':
        results[4] = 1
    elif residue == 'Q':
        results[5] = 1
    elif residue == 'E':
        results[6] = 1
    elif residue == 'G':
        results[7] = 1
    elif residue == 'H':
        results[8] = 1
    elif residue == 'I':
        results[9] = 1
    elif residue == 'L':
        results[10] = 1
    elif residue == 'K':
        results[11] = 1
    elif residue == 'M':
        results[12] = 1
    elif residue == 'F':
        results[13] = 1
    elif residue == 'P':
        results[14] = 1
    elif residue == 'S':
        results[15] = 1
    elif residue == 'T':
        results[16] = 1
    elif residue == 'W':
        results[17] = 1
    elif residue == 'Y':
        results[18] = 1
    elif residue == 'V':
        results[19] = 1
    else:
        results[20] = 1
        
    return results

# This function converts a protein sequence to a set of binary vectors 17x21

def convert_structure(structure):
    result = np.empty([17,21])
    for idx, entry in enumerate(structure):
        result[idx] = np.asarray(list(map(convert_residue, entry)));
    return result


# Convert output to a 2x1 vector, [1,0] beta-sheet, [0,1] alpha-helix, [0,0] not decided

def convert_output(out):
    o = []
    if out < 1.5:
        o = [1,0]
    elif out > 2.8:
        o = [0,1]
    else:
        o = [0,0]
    return o

# Function that converts a NN output to a binary vector according to a threshold

def apply_threshold(out):
    o = []
    if ( out[0] >= 0.3 and out[1] < 0.3):
        o = [1,0]
    elif ( out[0] < 0.37 and out[1] >= 0.37):
        o = [0,1]
    else:
        o = [0,0]
    return o

# This function is used later for confusion matrix, 1 - beta-sheet, 2 - alpha-helix, 3 - coil

# def apply_threshold_confusion(out):
#     o = []
#     if np.array_equal(out, [1,0]):
#         o = 1
#     elif np.array_equal(out, [0,1]):
#         o = 2
#     else:
#         o = 3
#     return o

#load data
X, y = dspp.load_data()

# add empty slots" to the beginning and the end of our protein:

for i, entry in enumerate(X):
    X[i]=np.insert(X[i],0, [' ',' ',' ',' ',' ',' ',' ',' ']);
    X[i]=np.insert(X[i], np.size(X[i]), [' ',' ',' ',' ',' ',' ',' ',' ']) ;


# relabel our output to convert N -> NxN:

y_relabelled = np.empty_like(y);
for idx, entry in enumerate(y):
    y_relabelled[idx]= list(map(convert_output, entry));
X_train, X_test, y_train, y_test = train_test_split(X, y_relabelled, test_size=0.3, random_state=12)

X_train3d=np.zeros((1,17,21))
for idx, entry in enumerate(X_train):
    Output = hankel(entry, entry[:17])
    Output = Output[:-16]
    for i, row in enumerate(Output):
        input = convert_structure(row)
        # X_train3d=np.vstack((X_train3d,input[None]))
        X_train3d=np.concatenate((X_train3d,input[None]),axis=0)
             
              
# sample_case_residue = hankel(X_test[0], X_test[0][:17])
# sample_case_residue = sample_case_residue[:-16]
# sample_case_residue = convert_input(sample_case_residue[0])

#print("Input: \n" + str(sample_case_residue))
#print("Output: \n" + str(output))
#print("Converted output: \n" + str(apply_threshold(output)))
