# The Anagram Problem
# CS 470/670 at UMass Boston - Midterm Exam 2020
import copy
global num_iterations

def anagram_expand(state, goal):
    node_list = []
    
    for pos in range(len(state) - 1):   # Create each possible state that can be created from the current one in a single step
        new_state = state[:pos] + state[-1:] + state[pos:-1]
    
        # Very simple h' function - please improve!
        # if new_state == goal:
        #     score = 0
        # else:
        #     score = 1
        # score=0
        # for i in range(len(goal)):
        #     if new_state[i] != goal[i]:
        #         score = score+1
        score=0
        score_list=[]
        goal_cp=copy.deepcopy(goal)
        char='a'
        for i in range(len(goal)):
            aa=new_state[i]
            j=goal_cp.index(aa)
            goal_cp = goal_cp[:j] + char + goal_cp[j + 1:]  
            if i<j:
                score_list.append(j-i);
            if i>j:
                score_list.append(len(goal)-1-i+1);
        if score_list != []:
            score=max(score_list)
        
        node_list.append((new_state, score))
    
    return node_list
                
def a_star(start, goal, expand):
    global num_iterations
    
    open_list = [([start], -1)]
    while open_list:
        num_iterations += 1
        open_list.sort(key = lambda x: len(x[0]) + x[1])
        if open_list[0][1] == 0:
            return open_list[0][0]
        
        ancestors = open_list[0][0]
        open_list = open_list[1:]
        new_nodes = expand(ancestors[-1], goal)
        
        for (new_state, score) in new_nodes:    
            append_new_node = True
            for ancestor in ancestors:
                if new_state == ancestor:       # Modified from Assignment #2 solutions to avoid numpy 
                    append_new_node = False
                    break
            
            if append_new_node:
                open_list.append((ancestors + [new_state], score))        
    return []

# Finds a solution, i.e., a placement of all rectangles within the given field, for a rectangle puzzle
def anagram_solver(start, goal):
    global num_iterations
    num_iterations = 0
    
    # Add code here to check in advance whether the problem is solvable
    sorted_start=sorted(start)
    sorted_goal=sorted(goal)
    if sorted_start!=sorted_goal:
        print('This is clearly impossible. I am not even trying to solve this.')
        return
        
    solution = a_star(start, goal, anagram_expand)
    
    if not solution:
        print('No solution found. This is weird, I should have caught this before even trying A*.')
        return
        
    print(str(len(solution) - 1) + ' steps from start to goal:')
    
    for step in solution:
        print(step)
    
    print(str(num_iterations) + ' A* iterations were performed to find this solution.')
    

#anagram_solver('CRATE', 'TRACE')

#anagram_solver('RESCUE', 'SECURE')

#anagram_solver('PREDATOR', 'TEARDROP')

anagram_solver('SCHOOLMASTER', 'THECLASSROOM')
