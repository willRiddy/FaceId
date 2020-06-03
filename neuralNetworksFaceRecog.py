#A neural network, hopefully turn into custom library

import numpy as np
import scipy.special

class Supervised:

    # initialise the neural network
    def __init__(self, inputnodes, hiddenlayer, outputnodes, learningrate): # hiddenlayer needs an array as an input
        # set number of nodes in each input, hidden, output layer
        self.inodes = inputnodes
        self.hlayer = hiddenlayer
        self.onodes = outputnodes

        self.weights = []
        self.hidden_outputs = []

        # learning rate
        self.lr = learningrate

        # activation function is the sigmoid function
        self.activation_function = lambda x: scipy.special.expit(x)

    def createWeights(self):
        # creates all the weights
        for i, nodes in enumerate(self.hlayer):
            if i == 0: # for the input nodes to the first layer of hidden nodes
                prevNodes = self.inodes
                weights = (np.random.normal(0.0, pow(prevNodes, -0.5), (nodes, prevNodes)))
            else:
                prevNodes = self.hlayer[i-1]
                weights = (np.random.normal(0.0, pow(prevNodes, -0.5), (nodes, prevNodes)))
            self.weights.append(weights)
        prevNodes = self.hlayer[-1]
        weights = (np.random.normal(0.0, pow(prevNodes, -0.5), (self.onodes, prevNodes)))
        self.weights.append(weights)

    def train(self, inputs_list, targets_list):
        # converts inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        # loop to calculate weights up to a certain point
        for i, weights in enumerate(self.weights):
            if i == 0: # calculates signals from input layer into hidden layer
                hidden_inputs = np.dot(self.weights[i], inputs)
            elif i == len(self.weights)-1: # when we get to the last weights we break from the loop
                break
            else: # calculate signals between hidden layers
                hidden_inputs = np.dot(self.weights[i], hidden_outputs)
            hidden_outputs = self.activation_function(hidden_inputs)
            self.hidden_outputs.append(hidden_outputs)
            
        # calculate signals emerging from hidden layer        
        final_hidden_outputs = self.activation_function(hidden_inputs)
        # calculate signals into final output layer
        final_inputs = np.dot(self.weights[-1], final_hidden_outputs)
        # calculate signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        # error is the target - actual
        output_errors = targets - final_outputs

        # hidden layer error is the output_errors, split by weights, recombined at hidden nodes
        # work out error for all the hidden layers
        errors = []
        for i, weight in reversed(list(enumerate(self.weights))):
            hidden_outputs = self.hidden_outputs[-(i+1)]
            if i == 0: # work out the error
                error = np.dot(weight.T, output_errors)
                # change the weights
                weight += self.lr * np.dot((output_errors * final_outputs * (1.0 - final_outputs)), np.transpose(error))
            elif i == len(self.weights)-1: # work out error from hidden to inputs
                error = np.dot(weight.T, error)
                # change the weights
                weight += self.lr * np.dot((error * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(inputs))
            else: # work out error
                error = np.dot(weight.T, error)
                # change the weights
                weight += self.lr * np.dot((error * hidden_outputs * (1.0 - hidden_outputs)), np.transpose(errors[-(i+1)]))
            errors.append(error)

    #query the neural network
    def query(self, inputs_list):
        # convert inputs list to 2d array
        inputs = np.array(inputs_list, ndmin=2).T

        # loop to calculate weights up to a certain point
        for i, weights in enumerate(self.weights):
            if i == 0: # calculates signals from input layer into hidden layer
                hidden_inputs = np.dot(self.weights[i], inputs)
            elif i == len(self.weights)-1: # when we get to the last weights we break from the loop
                break
            else: # calculate signals between hidden layers
                hidden_inputs = np.dot(self.weights[i], hidden_outputs)
            hidden_outputs = self.activation_function(hidden_inputs)

        #calculate signals into final output layer
        final_inputs = np.dot(self.who, hidden_outputs)
        # calculate the signals emerging from final output layer
        final_outputs = self.activation_function(final_inputs)

        return final_outputs
