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

def convert_input(sequence):
    aa_code = 'ACDEFGHIKLMNPQRSTVWY '
# define a mapping of chars to integers
    char_to_int = dict((c, i) for i, c in enumerate(aa_code))
# integer encode input data
    integer_encoded = [char_to_int[char] for char in sequence]
# one hot encode
    onehot_encoded = list()
    for value in integer_encoded:
        letter = [0 for _ in range(len(aa_code))]
        letter[value] = 1
        onehot_encoded.append(letter)
    onehot_encoded = np.asarray(onehot_encoded)
    return onehot_encoded


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
#X_train, X_test, y_train, y_test = train_test_split(X, y_relabelled, test_size=0.3, random_state=12)

X_input = np.empty_like(X);
for idx, entry in enumerate(X):
    Output = hankel(entry, entry[:17])
    Output = Output[:-16]
    for i, row in enumerate(Output):
        input = convert_input(row)
#    X_input[idx] =  input
             
              
# sample_case_residue = hankel(X_test[0], X_test[0][:17])
# sample_case_residue = sample_case_residue[:-16]
# sample_case_residue = convert_input(sample_case_residue[0])

#print("Input: \n" + str(sample_case_residue))
#print("Output: \n" + str(output))
#print("Converted output: \n" + str(apply_threshold(output)))
