import numpy as np
from dsppkeras.datasets import dspp
from scipy.linalg import hankel
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
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
        result[idx] = np.asarray( map(convert_residue, entry));
    return result

# Convert output to a 2x1 vector
# [1,0] beta-sheet
# [0,1] alpha-helix
# [0,0] not decided


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

# This function is used later for confusion matrix 
# 1 - beta-sheet
# 2 - alpha-helix
# 3 - coil

def apply_threshold_confusion(out):
    o = []
    if np.array_equal(out, [1,0]):
        o = 1
    elif np.array_equal(out, [0,1]):
        o = 2
    else:
        o = 3
    return o
class Neural_Network(object):
    def __init__(self):
        # I define 3 layers: input layer with 21 node ; hidden layer with 2 nodes; output layer with 2 nodes
        self.inputSize = 21
        self.outputSize = 2
        self.hiddenSize = 2
        # I randomly assign initial weights
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)
        
    def forward(self, X):
        # We perform a forward propagation through our network
          self.z = np.dot(X, self.W1) # product of X and W1 matricies
          self.z2 = self.sigmoid(self.z) # apply activation function
          self.z3 = np.dot(self.z2, self.W2) # product of hidden layer and W2 matricies
          o = self.sigmoid(self.z3) # final activation function
          #all shapes here are (17,2)
          return o
        
    def sigmoid(self, s):
    # activation function
      return 1/(1+np.exp(-s))
    
    def sigmoidPrime(self, s):
        #derivative of sigmoid
        return s * (1 - s)
    
    def backward(self, X, y, o):
    # backward propagation
        self.o_error = y - o # compute error
        self.o_delta = self.o_error*self.sigmoidPrime(o) # applying derivative of sigmoid to error
        self.z2_error = self.o_delta.dot(self.W2.T) # calculate z2 error
        self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2) # applying derivative of sigmoid to z2 error
        self.W1 += np.dot(np.transpose(X), self.z2_delta) # adjusting 1st set of weights
        self.W2 += np.dot(np.transpose(self.z2), self.o_delta) # adjusting 2nd set of weights

    def train(self, X, y):
        # train our network
        o = self.forward(X)
        self.backward(X, y, o)

    def saveWeights(self):
        #printing weights
        np.savetxt("1st_set_of_weights.txt", self.W1, fmt="%s")
        np.savetxt("2nd_set_of_weights.txt", self.W2, fmt="%s")

NN = Neural_Network()
#load data
X, y = dspp.load_data()

# add empty slots" to the beginning and the end of our protein:

for i, entry in enumerate(X):
    X[i]=np.insert(X[i],0, [' ',' ',' ',' ',' ',' ',' ',' ']);
    X[i]=np.insert(X[i], np.size(X[i]), [' ',' ',' ',' ',' ',' ',' ',' ']) ;


# relabel our output to convert N -> NxN:

y_relabelled = np.empty_like(y);
for idx, entry in enumerate(y):
    y_relabelled[idx]= map(convert_output, entry);
X_train, X_test, y_train, y_test = train_test_split(X, y_relabelled, test_size=0.3, random_state=12)

# Train our net for 100 cycles:

for cycle in range(1):

    for idx, entry in enumerate(X_train):
        Output = hankel(entry, entry[:17])
        Output = Output[:-16]
        for i, row in enumerate(Output):
              input = convert_structure(row)
              o = NN.forward(input)
              NN.train(input, y_train[idx][i])
NN.saveWeights()
sample_case_residue = hankel(X_test[0], X_test[0][:17])
sample_case_residue = sample_case_residue[:-16]
sample_case_residue = convert_structure(sample_case_residue[0])
output = NN.forward(sample_case_residue)[8]
print("Input: \n" + str(sample_case_residue))
print("Output: \n" + str(output))
print("Converted output: \n" + str(apply_threshold(output)))
