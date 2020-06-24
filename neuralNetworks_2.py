#A neural network, hopefully turn into custom library

import numpy as np
import scipy.special

class Supervised:

    # initialise the neural network
    def __init__(self, nodes, learningrate, weights=None):
        # set number of nodes in each input, hidden, output layer
        self.nodes = nodes
        self.nodesAdjust = nodes[1:]
        self.weights = []
        self.errorsList = []
        self.outputsList = []
        self.outputsListAdjusted = []
        self.bias = []

        # learning rate
        self.lr = learningrate

        if not weights:
            self.createWeights()
        else:
            self.weights = weights

        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

    def createWeights(self):

        for i, j in zip(self.nodes, self.nodesAdjust):
            weight = np.random.normal(0.0, pow(i, -0.5), (j, i)) # makes a random matrix for the weights
            self.weights.append(weight)
            bias = np.random.normal(0.0, pow(i, -0.5), (j, 1)) # makes a random column vector for the biases
            self.bias.append(bias)

    def train(self, inputs_list, targets_list):
        self.errorsList = []
        # converts targets list to 2d array
        targets = np.array(targets_list, ndmin=2).T

        error = targets - self.query(inputs_list) #primary error

        errWeights = self.weights[1:]  # dislodge everything by 1
        self.errorsList.insert(0, error)

        for weight in reversed(errWeights): # calculate hidden errors
            error = np.dot(weight.T, error)
            self.errorsList.insert(0, error)

        for weight, output, error, adjOutput in zip(self.weights, self.outputsList, self.errorsList, self.outputsListAdjusted):
            weight += self.lr * np.dot((error * adjOutput * (1-adjOutput)), np.transpose(output))  # back-prop algorithm

        for bias, adjOutput, error in zip(self.bias, self.outputsListAdjusted, self.errorsList):
            bias += self.lr * error * adjOutput * (1-adjOutput)


    def query(self, inputs_list):
        self.outputsList = []
        # convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T

        self.outputsList.append(inputs) #adds the input vector into the network

        for weight, bias in zip(self.weights, self.bias): #feeds through the network
            inputs = np.dot(weight, inputs) # feed forward
            inputs += bias
            inputs = self.activation_function(inputs) # uses sigmoid function
            self.outputsList.append(inputs)
        
        self.outputsListAdjusted = self.outputsList[1:]
        final_outputs = inputs #just to clarify

        return final_outputs