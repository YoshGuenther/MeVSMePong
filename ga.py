'''
Created on Mar 28, 2015
@author: Joshua Guenther
@author: Laura moyer
'''

from ann import *
import random
import pygame,sys
from pygame.locals import *

#Class representing a Genetic Algorithm
class GA():
    def __init__(self, display):
        self.gameScreen = display
        self.pop_size = 10#200
        self.generations = 5#100
        self.curGeneration = 0
        self.population = []
        for x in range(self.pop_size):
            self.population.append(ANN())

    def runGA(self):
        best = None
        self.curGeneration = 1
        #Run for the number of generations specified
        while self.curGeneration <= self.generations:
            self.render()
            #Calculate the fitness (play the game)
            count = 0
            for individual in self.population:
                print "Evaulating individual: "+str(count)+" ANN is: "+str(individual)
                count += 1
                self.evaluateANN(individual)


            #Compare fitness - Determine best and population to keep
            self.selectionSort(self.population)
            best = self.population[len(self.population)-1]
            self.population = self.population[self.pop_size/2 : len(self.population)] #keep top 50% of population, discard the rest

            new_population = [best]
            #Perform Variation (Mutation/CrossOver)
            for x in range(1, self.pop_size):
                if random.random() < 0.5:   # randomly pick a member of population, mutate, and add to new pop
                    child = random.choice(self.population).mutate()
                    new_population.append(child)
                else: #pick two random parents, perform crossover, and add child to population
                    p1 = random.choice(self.population)
                    p2 = random.choice(self.population)
                    child = p1.crossover(p2)
                    new_population.append(child)
            #update population with the new children
            self.population = new_population
            self.curGeneration += 1
            print "Best ANN is: "+str(best)
        #After completing every generation, return the best
        return best


    def evaluateANN(self, ann):
        game = GameManager(self.gameScreen, False, ann)
        game.gameLoop()
        ann.fitness = game.score
        game = None

    def selectionSort(self, array):
        for i  in range(len(array)-1):
            index = i
            for b in range(i+1, len(array)):
                if array[index] > array[b]:
                    index = b
            temp = array[i]
            array[i] = array[index]
            array[index] = temp

    def render(self):
        gameScreen = self.gameScreen
        gameScreen.fill((0, 0, 0))
        fontSize = 15
        font = pygame.font.Font(None, fontSize)
        x = int(gameScreen.get_width()/2) - 40
        y = int(gameScreen.get_height()/2)
        output = ["Running GA", "Generation: "+str(self.curGeneration)+"/"+str(self.generations), "Population Size: "+str(self.pop_size), "Best Fitness: "+str(self.population[0].fitness)]
        for s in range(len(output)):
            text = font.render(output[s], 1, (155,155,155))
            gameScreen.blit(text, (x, y + (s * fontSize)))
        pygame.display.update()
