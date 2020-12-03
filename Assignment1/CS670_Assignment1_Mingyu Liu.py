#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 23:41:00 2020

@author: Mingyu Liu
"""

# An Even More General Backtracking Function and its Application to the n-Queens Problem
# Assignment #1 for CS 470/670 at UMass Boston

import copy
import numpy as np

example_1 = np.array([[1, 0, 8, 5, 3, 0, 7, 0, 0],
                      [2, 0, 6, 0, 0, 8, 0, 3, 0],
                      [0, 0, 0, 0, 0, 4, 2, 5, 8],
                      [0, 0, 0, 0, 0, 5, 8, 1, 0],
                      [4, 2, 0, 0, 0, 0, 0, 6, 3],
                      [0, 8, 3, 2, 0, 0, 0, 0, 0],
                      [3, 6, 2, 4, 0, 0, 0, 0, 0],
                      [0, 7, 0, 6, 0, 0, 3, 0, 9],
                      [0, 0, 4, 0, 7, 3, 6, 0, 5]])

example_2 = np.array([[0, 0, 0, 0, 3, 0, 2, 8, 0],
                      [7, 0, 0, 5, 0, 0, 0, 1, 0],
                      [3, 0, 0, 0, 6, 0, 0, 0, 0],
                      [0, 8, 0, 0, 0, 2, 0, 4, 0],
                      [1, 0, 0, 0, 5, 0, 0, 0, 2],
                      [0, 6, 0, 9, 0, 0, 0, 3, 0],
                      [0, 0, 0, 0, 2, 0, 0, 0, 4],
                      [0, 4, 0, 0, 0, 6, 0, 0, 1],
                      [0, 9, 2, 0, 7, 0, 0, 0, 0]])


# "Sanity check" function for the sudoku problem.
# For a given search state (node), it checks whether the next decision could possibly lead to a solution 
def sudoku_check(current_state, decision_info, next_option):
    #checking in the row
    for i in range(0,9):
        #checking if there is a cell with same value
        if current_state[decision_info[0]][i] == next_option:
            return (False,None)
    #checking in the column
    for i in range(0,9):
        if current_state[i][decision_info[1]] == next_option:
            return (False,None)
    #finding topleft x,y co-ordinates of the submatrix that containing the decision_info cell
    topleft_row = (decision_info[0]//3)*3
    topleft_col = (decision_info[1]//3)*3;
    #checking submatrix 
    for i in range(topleft_row,topleft_row+3):
        for j in range(topleft_col,topleft_col+3):
            #checking if there is a cell with same value 
            if current_state[i][j] == next_option:
                return (False,None)
    new_state = copy.deepcopy(current_state)
    new_state[decision_info] = next_option
    return (True, new_state) 
        
        
# Recursive backtracking function that receives the options for the problem's sequence of decisions,
# a reference to a "sanity check" function and, optionally, the current search path.
# It returns the result as a pair (success indicator, list of n row indices for queen placement).
def backtrack(decision_seq, check_func, current_state, depth=0):
    for next_option in decision_seq[depth][1]:
        (success, new_state) = check_func(current_state, decision_seq[depth][0], next_option)
        #print('  ' * depth + 'Check state ' + str(current_state) + ' with next option ' + str(next_option) + '-> ' + str(success))
        if success and depth < len(decision_seq) - 1:
            (success, new_state) = backtrack(decision_seq, check_func, new_state, depth + 1)
        if success:
            return (True, new_state)
    return (False, None)


# Finds a solution for the sudoku problem.
def sudoku_solver(matrix):
    initial_state = matrix
    decision_seq=[]
    for i in range(0,9):
        for j in range (0,9):
            #check every cell to find cells that are unassigned
            if matrix[i][j] == 0:
                row = i
                col = j
                ds = ((row, col),list(range(1, 10))) 
                #add each decision sequence into decision_seq
                decision_seq.append(ds)
    return backtrack(decision_seq, sudoku_check, initial_state)

#Print sudoku result in a nice way
def sudoku_print(matrix):
    (success, solution) = sudoku_solver(matrix)
    if not success:
        print('Sorry, there is no solution to this sudoku problem.')
    else:
        print("\n")
        for i in range(len(solution)):
            line = ""
            if i == 3 or i == 6:
                print("---------------------")
            for j in range(len(solution[i])):
                if j == 3 or j == 6:
                    line += "| "
                line += str(solution[i][j])+" "
            print(line)


sudoku_print(example_1)
sudoku_print(example_2)