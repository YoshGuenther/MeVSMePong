'''
Created on Mar 28, 2015

@author: JGuenther
'''
import random
from gameObjects import *

#Class representing an Artifcial Neural Network
class ANN():
    #static variables
    problemSize = 3
    
    def __init__(self, nodeWeights=[]):
        #Need list so we are not referencing what is passed in
        self.nodeWeights = list(nodeWeights)
        random.seed()
        if len(self.nodeWeights) == 0:
            #Randomly initialize the weights of the nodes
            for n in range(0, ANN.problemSize):
                rnd = (random.random()*2)-1
                self.nodeWeights.append(rnd)
        self.fitness = 0
    
    # Create and return a copy of itself
    def copy(self): 
        newIndiv = ANN(self.nodeWeights[:])
        return newIndiv

    #Make a copy and randomly mutate one element in the new copy
    def mutate(self):
        newIndiv = self.copy()
        weightToMutate = random.randint(0, ANN.problemSize-1)
        newIndiv.nodeWeights[weightToMutate] += random.uniform(-1,1)
        return newIndiv

    #For each weight, randomly pick from which parent it comes from
    def crossover(self, other):
        new_indiv = ANN()
        for w in range(0, ANN.problemSize):
            if random.random() > 0.5:
                new_indiv.nodeWeights[w] = self.nodeWeights[w]
            else:
                new_indiv.nodeWeights[w]= other.nodeWeights[w]
        return new_indiv
    
    #Represents the Object when it it printed out
    def __repr__(self):
        return '{}: {} {}'.format(self.__class__.__name__, self.nodeWeights, self.fitness)

    #Used by Python to compare Objects
    def __cmp__(self, other):
        if hasattr(other, 'fitness'):
            return self.fitness.__cmp__(other.fitness)

    def run(self, inputs):
        totalSignal = 0.0
        for w in range(ANN.problemSize-1):
            sum = self.nodeWeights[w] * inputs[w]
            totalSignal += sum
        z = self.sigmoid(totalSignal)
        threshold = (1.0/5.0)
        if z > threshold:
            return 1.0
        elif threshold >= z and z >= -threshold:
            return 0
        else:
            return -1.0

    def sigmoid(self, z):
        return (2/(1+math.exp(-(1/5.0)*z)))-1

    # A single neuron with n weights
    class Neuron:
        def __init__(self, numWeights=4):
            self.weights = self.intializeWeights(numWeights)

        def intializeWeights(self, numWeights):
            newWeights = []
            for w in range(0, numWeights):
                randValue = random.uniform(-1.0,1.0)
                newWeights.append(randValue)
            return newWeights
        
        # Given inputs, sum up the signal and activate if above 0, or send -1
        
    